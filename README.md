# Google Images Scraper
Scrape Google Images effortlessly with this Python-based tool, using Selenium and the Chrome WebDriver.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)


Python (3.x recommended)
Chrome Web Browser (for the Chrome WebDriver)
Steps:

Clone the repository:
git clone [https://github.com/timadeg/google-image-scraper]

Navigate to the project directory and install the required packages:
cd google-image-scraper
pip install -r requirements.txt

Usage
To use the scraper, run the google_image_scraper.py file with the appropriate arguments:

python google_image_scraper.py "<SEARCH_TERM>" <NUMBER_OF_IMAGES> --start_index=<STARTING_INDEX>

Example:

python google_image_scraper.py "apple fruit" 50 --start_index=10

Features
Efficient Scraping: Uses Selenium to interact with the web page dynamically and fetch desired content.
Consent Handling: Automatically detects and handles consent forms on Google Images.
Customizability: Decide the number of images and the starting index.

Contributing
We welcome contributions! Please create an issue or submit a pull request if you'd like to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


# google-image-scraper
