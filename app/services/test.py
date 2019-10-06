def main():
    url = "https://rest.apisandbox.zuora.com"
    endpoint = "v1/transactions/payments/accounts/ff1e23e2211fb802b818d7c630fbc4f6"
    print(url.join(endpoint))


    print ("\n-------\n")
    print(url+endpoint)




if __name__ == '__main__':
    main()