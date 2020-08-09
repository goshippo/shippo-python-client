import shippo

'''
In this example we create a webhook, list the account webhooks, update the
 webhook, and delete the webhook.  More information regarding webhooks is
located in Shippo's API documetation https://goshippo.com/docs/webhooks/

Webhook endpoints must respond with a 200 http response. Basic Auth is not
supported.
'''

# Replace <API-KEY> with your key
shippo.config.api_key = <API-KEY>

account_webhooks = shippo.Webhook.list_webhooks()
print(account_webhooks)

new_webhook = shippo.Webhook.create(url='https://exampledomain.com', event='transaction_created')

# Repsonse contains the object_id (the identifier) of the webhook
print(new_webhook)

# update webhook event to all and change URL
# you could print(update_webhook) to see response info
update_webhook = shippo.Webhook.update(object_id=new_webhook.object_id,url='https://somenewurl.com', event='all',is_test=False)


# Retreieve list of all wehbooks
account_webhooks = shippo.Webhook.list_webhooks()
print(account_webhooks)


# delete the webhook (HTTP DELETE method) 
remove_webhook = shippo.Webhook.delete(object_id=webhook_object_id)

# see that webhook has been deleted
account_webhooks = shippo.Webhook.list_webhooks()
print(account_webhooks)
