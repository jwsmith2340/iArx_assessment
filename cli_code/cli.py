import requests
from time import sleep


def get_coordinates_from_user() -> tuple[int] | None:
    """Prompts the user for x and y coordinates.
    
        Args:
            None

        Returns:
            tuple: Two integers, the x and y input coordinates
    
    """
    try:
        x = int(input("Enter x coordinate (-10 to 10): "))
        y = int(input("Enter y coordinate (-10 to 10): "))
        if not (-10 <= x <= 10) or not (-10 <= y <= 10):
            print("Coordinates must be between -10 and 10.")
            return None, None
        return x, y

    except ValueError:
        print("Invalid input. Please enter valid integers for x and y.")
        return None, None


def query_api(x, y):
    """Sends a GET request to the FastAPI service and returns the response.
    
        Args:
            x (int): x coordinate gathered from user input
            y (int): y coordinate gathered from user input
        
        Returns:
            Json response object
    
    """
    api_url = f"http://app:5000/enter_coordinates/?x_axis={x}&y_axis={y}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error contacting the API: {e}")
        return None


def main() -> None:
    """Main function to prompt user and interact with FastAPI.
    
        Args:
            None

        Returns:
            None

    """
    while True:
        x, y = get_coordinates_from_user()

        if x is not None and y is not None:
            result = query_api(x, y)

            if result:
                print(f"Closest Central Fills to ({x}, {y}):")

                for station in result:
                    
                    print(
                        f"Central Fill {station['central_fill']:03d} - ${station['cheapest_medication']['med_price']:.2f}\tMedication: {station['cheapest_medication']['med_name'].upper()}\tDistance: {station['manhattan_distance']}"
                    )

        # Ask the user if they want to continue or exit
        continue_prompt = (
            input("Do you want to enter another coordinate? (y/n): ").strip().lower()
        )

        if continue_prompt != "y":
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
