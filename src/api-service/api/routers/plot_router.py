# src/api-service/api/routers/plot_router.py
from fastapi import APIRouter, HTTPException, Query
from starlette.responses import JSONResponse
from utils.tools.stockplotter import StockPlotter
import json

plot_router = APIRouter()

@plot_router.get("/plot_stock_prices")
def plot_stock_prices_endpoint(
    companies: str,
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    """
    Generates a plotly figure JSON for the given companies between the provided date range.
    companies: A comma-separated list of tickers.
    """
    company_list = [c.strip() for c in companies.split(",")]
    plotter = StockPlotter()
    fig = plotter.plot_stock_prices(
        companies=company_list, 
        start_date=start_date, 
        end_date=end_date,
        return_type="figure"
    )
    if isinstance(fig, str):
        # It's an error message
        raise HTTPException(status_code=400, detail=fig)

    # Convert the figure to JSON
    fig_json = fig.to_json()
    return JSONResponse(content=json.loads(fig_json))
