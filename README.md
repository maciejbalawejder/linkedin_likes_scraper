# LinkedIn Post Analytics Scraper🎨

A Python web scraper that LinkedIn post URLs, extracts the reaction count from each post, and saves posts that exceed a specified minimum likes threshold.

![](https://github.com/maciejbalawejder/linkedin_likes_scraper/blob/main/img/overview.png)

## How to use it? 
### 1. Git clone the repo
Copy the following code to your terminal
```
git clone https://github.com/maciejbalawejder/linkedin_likes_scraper.git
```
### 2. Create venv in the cloned folder
Go to linkedin_likes_scraper folder and run the following command

**2.1 Create Virtual Environment**
```bash
python -m venv linkedin_env
```
**2.2 Activate Virtual Environment**
- Windows
```bash
linkedin_env\Scripts\activate
```
- Mac/Linux
```bash
source linkedin_env\Scripts\activate
```
**2.3 Install dependencies**
```bash
pip install pandas requests tqdm
```
**2.4 Deactivate the env when you're done**
```bash
deactivate
```
### 3. Export/Download Posts from Octolenses
Export your Linkedin posts in Octolens.
![](https://github.com/maciejbalawejder/linkedin_likes_scraper/blob/main/img/octolens_download.png)

### 4. Run the scraper
Go to the linkedin_likes_scraper folder, and run the following command with the path to your Octolens csv file. When the script finishes running, it will create a new CSV file in the same folder as the original file.
```bash
python run.py path_to_your_octolens_csv
```
![](https://github.com/maciejbalawejder/linkedin_likes_scraper/blob/main/img/completed_run.png)
