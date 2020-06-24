from bsedata.bse import BSE

def getCurrentPrice(stockCode):   # stockCode must be a code in String, eg. '500325'
	if(type(stockCode) != str):
		return 'Stock code should be a string'

	b = BSE(update_codes = True)

	try:
		stockDetails = b.getQuote(stockCode)
		return float(stockDetails['currentValue'])
	except AttributeError:
		return 'Not a valid stock code'
