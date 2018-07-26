import cashaddress

legacy_dest_addr = "mvvfzV7QLHRwTb64SXVuKSGn17wbPNB2aW"
print(legacy_dest_addr)

dest_addr = cashaddress.convert.to_cash_address(legacy_dest_addr)
print(dest_addr)
