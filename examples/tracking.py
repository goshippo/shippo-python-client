import shippo

'''
In this tutorial we have an order with a sender address,
recipient address and parcel information that we need to ship.
'''

# Replace <API-KEY> with your key
shippo.config.api_key = "<API-KEY>"

# Tracking based on a Shippo transaction
transaction_id = '<TRANSACTION-ID>'
transaction = shippo.Transaction.retrieve(transaction_id)

if transaction:
    print(transaction.get('tracking_status'))
    print(transaction.get('tracking_history'))

# Tracking based on carrier and tracking number
tracking_number = '9205590164917337534322'
# For full list of carrier tokens see https://goshippo.com/docs/reference#carriers
carrier_token = 'usps'
tracking = shippo.Track.get_status(carrier_token, tracking_number)
print(tracking)

# Registering a tracking webhook
webhook_response = shippo.Track.create(
    carrier=carrier_token, 
    tracking_number=tracking_number, 
    metadata='optional, up to 100 characters'
)
print webhook_response

#For more tutorals of address validation, tracking, returns, refunds, and other functionality, check out our
#complete documentation: https://goshippo.com/docs/
