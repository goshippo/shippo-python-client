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

# Create a webhook endpoint (FYI-basic auth not supported) 
# For a full list of Webhook Event Types see https://goshippo.com/docs/webhooks/
new_webhook_response = shippo.Webhook.create(url='https://exampledomain.com',event='all') 
print(new_webhook_response)

# list webhook(s)
webhook_list = shippo.Webhook.list_webhooks()
print(webhook_list)

# remove all webhooks
for webhook in webhook_list['results']:
    print("about to delete webhook {}".format(webhook['object_id']))
    webhook_remove = shippo.Webhook.delete(object_id=webhook['object_id'])
    # print empty 204 status
    print(webhook_remove)


# Registering a tracking number for webhook
webhook_response = shippo.Track.create(
    carrier=carrier_token,
    tracking_number=tracking_number,
    metadata='optional, up to 100 characters'
)

print(webhook_response)

# For more tutorals of address validation, tracking, returns, refunds, and other functionality, check out our
# complete documentation: https://goshippo.com/docs/
