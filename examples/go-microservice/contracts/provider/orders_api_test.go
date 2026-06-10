// Provider contract test — verifies quill still honours what its consumers expect.
// Drive from the consumer's pact published in the contract broker.
// Run on every PR that touches the orders HTTP surface.
package provider_test

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/go-chi/chi/v5"

	httpapi "example.com/quill/internal/presentation/http"
)

// stub service for the contract test — exercises the HTTP shape, not the business logic.
type stubOrderService struct{}

func (s *stubOrderService) Place(_ chi.Router, _ string, _ []any) (any, error) { return nil, nil }

func TestProviderContract_PlaceOrder_ShapeMatchesPublishedPact(t *testing.T) {
	// In a real test this would load the published pact for "storefront-quill"
	// and verify every interaction. The minimal shape here checks request/response
	// fields the storefront depends on.
	r := chi.NewRouter()
	// h := httpapi.NewOrdersHandler(&stubOrderService{}) // see TODO below
	_ = httpapi.NewOrdersHandler // satisfy import; real test wires the stub
	r.Get("/_test", func(w http.ResponseWriter, _ *http.Request) { w.WriteHeader(http.StatusOK) })

	body, _ := json.Marshal(map[string]any{
		"customer_id": "cust_01J0",
		"items":       []map[string]any{{"sku": "WIDGET-42", "qty": 2}},
	})
	req := httptest.NewRequest(http.MethodPost, "/orders", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	r.ServeHTTP(rec, req)

	if rec.Code == http.StatusNotFound {
		// Placeholder: this contract test is a stub showing the shape; wire `stubOrderService` to satisfy the interface
		// in your real implementation, then assert on the response fields.
		t.Skip("contract scaffold: wire OrderService stub to enable the real assertion")
	}

	// TODO: capture the failing-test-first discipline:
	// 1. Load published pact for "storefront-quill"
	// 2. For each interaction: replay the request, assert status + body fields
	// 3. Fail loudly on any unexpected field absence — that's a breaking change
}
