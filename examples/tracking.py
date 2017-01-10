import shippo

'''
In this tutorial we have an order with a sender address,
recipient address and parcel information that we need to ship.
'''

# Replace <API-KEY> with your key
shippo.api_key = "<API-KEY>"

# Tracking based on a Shippo transaction
transaction_id = '7774eff962dd4ae3ad125dceed5c4858'
transaction = shippo.Transaction.retrieve(transaction_id)

if transaction:
    print transaction.get('tracking_status')
    print transaction.get('tracking_history')

# Tracking based on carrier and tracking number
tracking_number = '9205590164917337534322'
# For full list of carrier tokens see https://goshippo.com/docs/reference#carriers
carrier_token = 'usps'
tracking = shippo.Tracking.get(carrier_token, tracking_number)
print tracking

# Registering a tracking webhook
webhook_response = shippo.Tracking.create_webhook(
                                        carrier=carrier_token, 
                                        tracking=tracking_number, 
                                        metadata='optional'
                                    )
print webhook_response

#For more tutorals of address validation, tracking, returns, refunds, and other functionality, check out our
#complete documentation: https://goshippo.com/docs/