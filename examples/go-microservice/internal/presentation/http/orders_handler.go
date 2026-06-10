// Package httpapi exposes the HTTP surface.
// Handlers are thin: validate, call service, format response.
package httpapi

import (
	"encoding/json"
	"errors"
	"net/http"

	"github.com/go-chi/chi/v5"

	"example.com/quill/internal/application/services"
	"example.com/quill/internal/domain"
)

type OrdersHandler struct {
	orders services.OrderService
}

func NewOrdersHandler(orders services.OrderService) *OrdersHandler {
	return &OrdersHandler{orders: orders}
}

func (h *OrdersHandler) Mount(r chi.Router) {
	r.Post("/orders", h.placeOrder)
}

type placeOrderRequest struct {
	CustomerID string         `json:"customer_id"`
	Items      []orderItemDTO `json:"items"`
}

type orderItemDTO struct {
	SKU string `json:"sku"`
	Qty int    `json:"qty"`
}

type placeOrderResponse struct {
	OrderID string `json:"order_id"`
	Status  string `json:"status"`
}

func (h *OrdersHandler) placeOrder(w http.ResponseWriter, r *http.Request) {
	var req placeOrderRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, "invalid_body")
		return
	}

	items := make([]domain.OrderLine, 0, len(req.Items))
	for _, it := range req.Items {
		items = append(items, domain.OrderLine{SKU: it.SKU, Qty: it.Qty})
	}

	order, err := h.orders.Place(r.Context(), req.CustomerID, items)
	switch {
	case errors.Is(err, services.ErrInvalidOrder):
		writeError(w, http.StatusBadRequest, "invalid_order")
	case errors.Is(err, services.ErrWarehouseUnavailable):
		writeError(w, http.StatusServiceUnavailable, "warehouse_unavailable")
	case err != nil:
		writeError(w, http.StatusInternalServerError, "internal_error")
	default:
		writeJSON(w, http.StatusCreated, placeOrderResponse{
			OrderID: order.ID.String(),
			Status:  string(order.Status),
		})
	}
}

func writeJSON(w http.ResponseWriter, code int, body any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	_ = json.NewEncoder(w).Encode(body)
}

func writeError(w http.ResponseWriter, code int, kind string) {
	writeJSON(w, code, map[string]string{"error": kind})
}
