from fastapi import HTTPException
import re

STATE_CODES = {
    "01": "Jammu & Kashmir",
    "02": "Himachal Pradesh",
    "03": "Punjab",
    "04": "Chandigarh",
    "05": "Uttarakhand",
    "06": "Haryana",
    "07": "Delhi",
    "08": "Rajasthan",
    "09": "Uttar Pradesh",
    "10": "Bihar",
    "11": "Sikkim",
    "12": "Arunachal Pradesh",
    "13": "Nagaland",
    "14": "Manipur",
    "15": "Mizoram",
    "16": "Tripura",
    "17": "Meghalaya",
    "18": "Assam",
    "19": "West Bengal",
    "20": "Jharkhand",
    "21": "Odisha",
    "22": "Chhattisgarh",
    "23": "Madhya Pradesh",
    "24": "Gujarat",
    "25": "Daman and Diu",
    "26": "Dadra and Nagar Haveli",
    "27": "Maharashtra",
    "28": "Andhra Pradesh (Old)",
    "29": "Karnataka",
    "30": "Goa",
    "31": "Lakshadweep",
    "32": "Kerala",
    "33": "Tamil Nadu",
    "34": "Puducherry",
    "35": "Andaman and Nicobar Islands",
    "36": "Telangana",
    "37": "Andhra Pradesh (New)",
    "38": "Ladakh"
}

class GSTStateName:

    @staticmethod
    async def get_state_from_gstin(data):
        print("api v2")
        gstin = data.gstNumber
        gstin = gstin.strip().upper()

        if not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', gstin):
            raise HTTPException(status_code=400, detail="Invalid GSTIN format")

        state_code = gstin[:2]
        state_name = STATE_CODES.get(state_code)

        if not state_name:
            raise HTTPException(status_code=404, detail="State code not found")

        return {
            "gstin": gstin,
            "state_code": state_code,
            "state_name": state_name,
            "filling_frequency":data.filingFrequency,
            "month":data.month,
            "year":data.year
        }
