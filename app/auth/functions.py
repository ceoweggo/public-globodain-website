from app.auth.models import Models

class Functions():

    class Requests:

        def request_business_demo(items):
            model_id = Models.Requests.business_demo(items)

            ## ADD TESTING MOCKS // MARIO
            return model_id