from locust import HttpUser, task


class LocustPerfTest(HttpUser):
    @task
    def index(self) -> None:
        self.client.get("")

    @task
    def show_summary(self) -> None:
        self.client.post("showSummary", data={"email": "admin@irontemple.com"})

    @task
    def book(self) -> None:
        self.client.get("book/Spring Festival/Simply Lift")

    @task
    def purchase_places(self) -> None:
        with self.client.post(
            "purchasePlaces",
            data={"competition": "Spring Festival", "club": "Simply Lift", "places": 1},
            catch_response=True,
        ) as response:
            if (
                response.status_code == 400
                and "Sorry you dont have anymore points." in response.text
            ):
                response.success()

    @task
    def display_board(self) -> None:
        self.client.get("displayBoard")

    @task
    def logout(self) -> None:
        self.client.get("logout")
