// Package health exposes /healthz (liveness) and /readyz (readiness).
//
// Liveness is "is the process alive?" — always 200 if the binary can serve a request.
// Readiness is "can this instance accept traffic right now?" — pings every hard dependency.
package health

import (
	"context"
	"encoding/json"
	"net/http"
	"time"
)

// ReadinessProbe pings hard dependencies. Implementations live in infrastructure/.
type ReadinessProbe interface {
	Ping(ctx context.Context) error
	Name() string
}

// Handler wires the two endpoints. Probes are injected at construction.
type Handler struct {
	probes  []ReadinessProbe
	timeout time.Duration
}

func NewHandler(probes []ReadinessProbe) *Handler {
	return &Handler{probes: probes, timeout: 500 * time.Millisecond}
}

// Liveness — always 200 unless the goroutine that serves it is gone.
func (h *Handler) Liveness(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "alive"})
}

// Readiness — pings every probe; 200 only if all succeed.
func (h *Handler) Readiness(w http.ResponseWriter, r *http.Request) {
	ctx, cancel := context.WithTimeout(r.Context(), h.timeout)
	defer cancel()

	failures := make(map[string]string)
	for _, p := range h.probes {
		if err := p.Ping(ctx); err != nil {
			failures[p.Name()] = err.Error()
		}
	}

	w.Header().Set("Content-Type", "application/json")
	if len(failures) == 0 {
		_ = json.NewEncoder(w).Encode(map[string]string{"status": "ready"})
		return
	}
	w.WriteHeader(http.StatusServiceUnavailable)
	_ = json.NewEncoder(w).Encode(map[string]any{"status": "not_ready", "failures": failures})
}
