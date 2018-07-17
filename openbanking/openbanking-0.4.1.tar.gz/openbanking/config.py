"""
No order.
"""
model_banks = [
    # ForgeRock Model Bank
    # dict(
    #     order=0,
    #     code=1,
    #     name="ForgeRock",
    #     support_url="https://www.forgerock.com",
    #     api_version="v1.1",
    #     well_known="https://as.aspsp.ob.forgerock.financial/oauth2/.well-known/openid-configuration",
    #     postman_collections=["https://github.com/ForgeRock/ForgeRock-OpenBanking-Sample/tree/master/postman"],
    #     resource_server="https://rs.aspsp.ob.forgerock.financial:443/open-banking/v1.1/",
    #     financial_id="0015800001041REAAY"
    #
    # ),
    # Ozone Model Bank
    dict(
        order=1,
        code=2,
        name="Ozone",
        support_url="https://ob.o3bank.co.uk/",
        api_version="v1.1",
        well_known="https://modelobankauth2018.o3bank.co.uk:4101/.well-known/openid-configuration",
        postman_collections=[
            "https://ob2018.o3bank.co.uk/postman/O3-Heimdall.postman_collection.json",
            "https://ob2018.o3bank.co.uk/postman/OpenBanking-AISP-v1.1.0.postman_collection.json"
        ],
        resource_server="https://modelobank2018.o3bank.co.uk:4501/open-banking/v2.0",
        financial_id="0015800001041RHAAY"


    ),
    # ForgeRock Model Bank using their own directory sandbox.
    # dict(
    #     order=0,
    #     code=3,
    #     name="ForgeRockDS",
    #     support_url="https://www.forgerock.com",
    #     api_version="v1.1",
    #     well_known="https://as.aspsp.integ-ob.forgerock.financial/oauth2/.well-known/openid-configuration",
    #     postman_collections=[""],
    #     resource_server="https://rs.aspsp.integ-ob.forgerock.financial:443/open-banking/v1.1/",
    #     financial_id="0015800001041REAAY"
    #
    # ),

]
