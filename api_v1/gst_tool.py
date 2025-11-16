import base64
import io
from typing import Optional
from controller.gst_controller import GSTController
from fastapi import APIRouter, Form, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse

from controller.gst_sheets.generate_json import generate_json
from controller.gst_sheets.gst_state import GSTStateName
from schemas.gst_schema import GSTDetailsForState
import pandas as pd

gst_router = APIRouter()

# @gst_router.post("/upload-excels")
# async def upload_excels(
#    tcs_sales_return: UploadFile = File(...),
#     tcs_sales: UploadFile = File(...),
#     tax_invoice_details: UploadFile = File(...),
#     gst_number: str = Form(...),
#     filing_frequency: Optional[str] = Form(None),
#     month: Optional[str] = Form(None),
#     quarter: Optional[str] = Form(None),
#     year: Optional[str] = Form(None)
# ):
#     return await GSTController.calculate_gst(
#         tcs_sales_return,
#         tcs_sales,
#         tax_invoice_details,
#         gstNumber=gst_number,
#         filingFrequency=filing_frequency,
#         month=month,
#         quarter=quarter,
#         year=year
#     )
@gst_router.post("/upload-excels")
async def upload_excels(
    tcs_sales_return: UploadFile = File(...),
    tcs_sales: UploadFile = File(...),
    tax_invoice_details: UploadFile = File(...),
    gst_number: str = Form(...),
    filing_frequency: Optional[str] = Form(None),
    month: Optional[str] = Form(None),
    quarter: Optional[str] = Form(None),
    year: Optional[str] = Form(None)
):
    try:
        result = await GSTController.calculate_gst(
            tcs_sales_return,
            tcs_sales,
            tax_invoice_details,
            gstNumber=gst_number,
            filingFrequency=filing_frequency,
            month=month,
            quarter=quarter,
            year=year
        )
        # print(f"API result: {result}")
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    
@gst_router.post("/get-gst-json")
async def get_gst_json(
    tcs_sales_return: UploadFile = File(...),
    tcs_sales: UploadFile = File(...),
    tax_invoice_details: UploadFile = File(...),
    gst_number: str = Form(...),
    filing_frequency: str = Form(...),
    month: str = Form(...),
    year: str = Form(...)
):
    try:
        # Read Excel files into DataFrames
        tcs_sales_df = pd.read_excel(io.BytesIO(await tcs_sales.read()))
        tcs_sales_return_df = pd.read_excel(io.BytesIO(await tcs_sales_return.read()))
        tax_invoice_details_df = pd.read_excel(io.BytesIO(await tax_invoice_details.read()))
        # Generate JSON data
        json_data =  generate_json(
            tcs_sales_df,
            tcs_sales_return_df,
            tax_invoice_details_df,
            gst_number,
            f"{month}{year}",
            version="GST3.1.6"
        )
        return JSONResponse(content=json_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSON generation failed: {str(e)}")

@gst_router.post("/get-state")
async def find_state(gst_state_Req:GSTDetailsForState):
    print("api v1")
    return await GSTStateName.get_state_from_gstin(gst_state_Req)
