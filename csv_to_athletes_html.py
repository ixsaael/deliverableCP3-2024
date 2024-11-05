import csv
import os

def generate_html_links(directory):
    links = []
    
    for filename in os.listdir(directory):
       if filename.endswith(".html"):
        link = f' <a href = "{filename}" > {filename} </a><br>'
        links.append(link)
        
    links_html = "\n".join(links)
    nav_links = f" <nav><details><summary>Men's Roster</summary>\n{links_html}\n</details></nav>" 
    
    return nav_links

dir = os.getcwd()
nav_html = generate_html_links(dir + "/mens_team")

def generate_html_links2(directory):
    links = []
    
    for filename in os.listdir(directory):
       if filename.endswith(".html"):
        link = f' <a href = "{filename}" > {filename} </a><br>'
        links.append(link)
        
    links_html = "\n".join(links)
    nav_links = f" <nav><details><summary>Womens's Roster</summary>\n{links_html}\n</details></nav>" 
    
    return nav_links

dir = os.getcwd()
nav_html2 = generate_html_links2(dir + "/womens_team")

def process_athlete_data(file_path):

   # Extracting athlete stats by year
   records = []

   # Extracting athlete races
   races = []           

   athlete_name = ""
   athlete_id = ""
   comments = ""

   with open(file_path, newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      data = list(reader)

      athlete_name = data[0][0]
      athlete_id = data[1][0]
      print(f"The athlete id for {athlete_name} is {athlete_id}")

      for row in data[5:-1]:
         if row[2]:
            records.append({"year": row[2], "sr": row[3]})
         else:
            races.append({
               "finish": row[1],
               "time": row[3],
               "meet": row[5],
               "url": row[6],
               "comments": row[7]
            })

   return {
      "name": athlete_name,
      "athlete_id": athlete_id,
      "season_records": records,
      "race_results": races,
      "comments": comments
   }    

def gen_athlete_page(data, outfile):
    # Start building the HTML structure with updated elements and classes
    html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- FontAwesome for icons (replace with actual FontAwesome ID) -->
    <script src="https://kit.fontawesome.com/YOUR_ID.js" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="../css/reset.css">
    <link rel="stylesheet" href="../css/style.css">
    <title>{data["name"]}</title>
</head>
<body data-theme="light">  <!-- Enables theme toggling -->
    <a href="#main" class="skip-link">Skip to Main Content</a>

    <!-- Theme toggle corner icons -->
    <div class="theme-toggle-icons">
        <button onclick="setTheme('light')" title="Light Mode">
            <i class="fas fa-sun"></i>
        </button>
        <button onclick="setTheme('dark')" title="Dark Mode">
            <i class="fas fa-moon"></i>
        </button>
        <button onclick="setTheme('high-contrast')" title="High Contrast">
            <i class="fas fa-adjust"></i>
        </button>
    </div>
    
    <!-- Navigation links -->
    <nav>
        <ul>
            <li><a href="./../index.html">Home Page</a></li>
            <li>{nav_html}</li>
            <li>{nav_html2}</li>
        </ul>
    </nav>

    <!-- Header with athlete name and profile image -->
    <header class="sticky-header">
        <h1>{data["name"]}</h1>
        <img src="../images/profiles/{data["athlete_id"]}.jpg" alt="Profile picture of {data["name"]}" class="athlete-profile">
    </header>

    <main id="main">
        <!-- Seasonal Records Section -->
        <section id="athlete-sr-table" class="table-container">
            <h2 class="section-title">Athlete's Seasonal Records (SR) per Year</h2>
            <table>
                <thead>
                    <tr>
                        <th>Year</th>
                        <th>Season Record (SR)</th>
                    </tr>
                </thead>
                <tbody>
    '''

    # Add rows for each season record
    for sr in data["season_records"]:
        html_content += f'''
                    <tr>
                        <td>{sr["year"]}</td>
                        <td>{sr["sr"]}</td>
                    </tr>
        '''

    html_content += '''
                </tbody>
            </table>
        </section>

        <!-- Race Results Section -->
        <section id="athlete-result-table" class="table-container">
            <h2 class="section-title">Race Results</h2>
            <table id="athlete-table">
                <thead>
                    <tr>
                        <th>Race</th>
                        <th>Athlete Time</th>
                        <th>Athlete Place</th>
                        <th>Race Comments</th>
                    </tr>
                </thead>
                <tbody>
    '''

    # Add each race as a row into the race table
    for race in data["race_results"]:
        html_content += f'''
                    <tr class="result-row">
                        <td><a href="{race["url"]}">{race["meet"]}</a></td>
                        <td>{race["time"]}</td>
                        <td>{race["finish"]}</td>
                        <td>{race["comments"]}</td>
                    </tr>
        '''

    html_content += '''
                </tbody>
            </table>
        </section>

        <!-- Gallery Section -->
        <section id="gallery">
            <h2 class="section-title">Gallery</h2>
            <!-- Add gallery content here -->
        </section>
    </main>

    <!-- Footer Section -->
    <footer>
        <p>
            Skyline High School<br>
            <address>
                2552 North Maple Road<br>
                Ann Arbor, MI 48103<br><br>
            </address>
            <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
            Follow us on Instagram <a href="https://www.instagram.com/a2skylinexc/"><i class="fa-brands fa-instagram" aria-label="Instagram"></i></a>
        </p>
    </footer>

    <!-- JavaScript for theme toggling -->
    <script>
        function setTheme(theme) {
            document.body.setAttribute('data-theme', theme);
        }
    </script>
</body>
</html>
    '''

    # Write the generated HTML content to the specified output file
    with open(outfile, 'w', encoding='utf-8') as output:
        output.write(html_content)



def main():

   import os
   import glob

   # Define the folder path
   folder_path = 'mens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("mens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "mens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")


   # Define the folder path
   folder_path = 'womens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("womens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "womens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")

if __name__ == '__main__':
    main()
