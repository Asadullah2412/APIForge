# converts others to QAR

# Conversion values where 1 unit of currency = X QAR
from fastapi import status
currencies_to_qar = {
    "USD": 3.65,    # 1 USD = 3.65 QAR
    "EUR": 3.91,    # Approx market rate
    "GBP": 4.62,    
    "AED": 0.99,    # UAE Dirham
    "SAR": 0.97     # Saudi Riyal
}

def currency_convertor(value:float,currency:str):
    
    if value > 0 :
        if currency.upper() in currencies_to_qar:
            QAR_value = currencies_to_qar.get(currency.upper()) * value
            return {"qar":QAR_value}
        else:
            return status.HTTP_404_NOT_FOUND                      
    else:
        return status.HTTP_400_BAD_REQUEST
        
