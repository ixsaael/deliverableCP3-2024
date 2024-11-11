import csv
import os
import re
import glob

def generate_html_links(directory, current_filename, team="mens"):
    """
    Generates HTML navigation links for a team (men or women) excluding the current profile.

    Parameters:
    - directory (str): Directory with team profile HTML files.
    - current_filename (str): Filename to exclude from navigation.
    - team (str): Either 'mens' or 'womens' for team specification.

    Returns:
    - str: HTML formatted navigation links.
    """
    links = []
    filename_sorted = sorted(os.listdir(directory))
    team_folder = "mens_team" if team == "mens" else "womens_team"
    nav_title = "Men's Roster" if team == "mens" else "Women's Roster"

    for filename in filename_sorted:
        if filename.endswith(".html") and filename != current_filename:
            display_name = re.sub(r'\d+$', '', os.path.splitext(filename)[0])
            link = f'<a href="./../{team_folder}/{filename}">{display_name}</a><br>'
            links.append(link)
    
    links_html = "\n".join(links)
    nav_links = f'<nav><details><summary class="nav-button">{nav_title}</summary>' \
                f'<div class="dropdown-content">\n{links_html}\n</div></details></nav>'
    return nav_links

def process_athlete_data(file_path):
    """
    Processes athlete CSV data to extract season records and race results.

    Parameters:
    - file_path (str): Path to the athlete's CSV file.

    Returns:
    - dict: Contains athlete's name, ID, seasonal records, race results, and comments.
    """
    records = []
    races = []
    athlete_name = ""
    athlete_id = ""
    
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

        athlete_name = data[0][0]
        athlete_id = data[1][0]
        print(f"The athlete ID for {athlete_name} is {athlete_id}")

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
        "comments": ""
    }

def gen_athlete_page(data, outfile):
    """
    Generates an HTML page for an athlete profile.

    Parameters:
    - data (dict): Athlete data with name, ID, seasonal records, and race results.
    - outfile (str): Output path for the generated HTML file.
    """
    # Generate navigation links for men and women teams
    nav_html_men = generate_html_links(os.path.join(os.getcwd(), "mens_team"), os.path.basename(outfile), "mens")
    nav_html_women = generate_html_links(os.path.join(os.getcwd(), "womens_team"), os.path.basename(outfile), "womens")
    
    sr_icon_html = '<span class="sr-symbol">🏃‍♂️👟</span>'
    pr_icon_html = '<span class="pr-symbol">⏱️⬆️</span>'

    # Build HTML content
    html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="stylesheet" href="../css/reset.css">
    <link rel="stylesheet" href="../css/style.css">
    <title>{data["name"]}</title>
</head>
<body data-theme="light">

    <div id="progress-bar-container">
        <div id="progress-bar"></div>
    </div>

    <!-- Navigation links -->
    <div class="button-row">
        <div onclick="toggleNav()">
            <details><summary class="nav-button">Content</summary>
        </div>
        {nav_html_men}
        {nav_html_women}
    </div>
    
    <!-- Sticky Horizontal Navigation -->
    <div class="sticky-nav" id="sticky-nav">
        <ul>
            <li><a href="./../index.html">Home</a></li>
            <li><a href="#header" class="skip-link">Profile</a></li>
            <li><a href="#athlete-sr-table" class="skip-link">Year Stats</a></li>
            <li><a href="#athlete-result-table" class="skip-link">Race Stats</a></li>
            <li><a href="#footer" class="skip-link">Other</a></li>
        </ul>
    </div>

    <!-- Header with athlete name and profile image -->
    <header id="header" class="sticky-header">
        <h1>{data["name"]}</h1>
        <img src="../images/profiles/{data["athlete_id"]}.jpg" alt="Profile picture of {data["name"]}" 
             tabindex="0" class="athlete-profile1" onclick="openLightbox(this.src)" 
             onerror="this.onerror=null; this.src='../images/default_image.jpg';">
    </header>
    
    <!-- Lightbox overlay structure -->
    <div class="lightbox" id="lightbox">
        <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
        <img id="lightbox-img" src="" alt="Enlarged profile image">
    </div>

    <main id="main">
        <!-- Seasonal Records Section -->
        <section id="athlete-sr-table" class="table-container">
            <h2 class="section-title">Athlete's Seasonal Records (SR) per Year</h2>
            <table>
                <thead>
                    <tr><th>Year</th><th>Season Record (SR)</th></tr>
                </thead>
                <tbody>
    '''
    for sr in data["season_records"]:
        # Replace "SR" and "PR" in the season record cells
        season_record = sr["sr"].replace("SR", sr_icon_html).replace("PR", pr_icon_html)
        html_content += f'''
                    <tr>
                        <td>{sr["year"]}</td>
                        <td>{season_record}</td>
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
                    <!-- Race Results Rows Here -->
    '''
    for race in data["race_results"]:
         # Replace "SR" and "PR" in the race results cells
        race_time = race["time"].replace("SR", sr_icon_html).replace("PR", pr_icon_html)
        html_content += f'''
                    <tr class="result-row">
                        <td><a href="{race["url"]}">{race["meet"]}</a></td>
                        <td>{race_time}</td>
                        <td>{race["finish"]}</td>
                        <td>{race["comments"]}</td>
                    </tr>
        '''
    html_content += '''
                </tbody>
            </table>
        </section>
        
        <!-- Legend Box for SR and PR icons -->
        <div class="legend-box">
            <div class="legend-item" tabindex="0" role="button" aria-label="School Record" onclick="scrollToSymbol('sr-symbol')">
                <span class="legend-icon">🏃‍♂️👟</span> SR - School Record
            </div>
            <div class="legend-item" tabindex="0" role="button" aria-label="Personal Record" onclick="scrollToSymbol('pr-symbol')">
                <span class="legend-icon">⏱️⬆️</span> PR - Personal Record
            </div>
        </div>
    </main>

    <!-- Footer Section -->
    <footer id="footer">
        <p>Skyline High School<br>
           <address>2552 North Maple Road<br>Ann Arbor, MI 48103</address>
           <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
           Follow us on <a href="https://www.instagram.com/a2skylinexc/">Instagram</a>
        </p>
    </footer>

    <div class="theme-toggle-container">
        <button class="toggle-arrow" onclick="toggleThemeOptions()">&#9650;</button>
        <div class="theme-options">
            <button onclick="setTheme('light')">Light</button>
            <button onclick="setTheme('dark')">Dark</button>
            <button onclick="setTheme('high-contrast')">High Contrast</button>
        </div>
    </div>

    <script>
    
    
    // Toggle the horizontal navigation bar on Content button click
        function toggleNav() {
            var nav = document.getElementById('sticky-nav');
            nav.classList.toggle('show'); // Toggle the visibility of the navigation bar
        }

        // Change Content button to Toggle button on scroll (optional for hiding)
        window.onscroll = function() {toggleContentButton()};

        function toggleContentButton() {
            var contentButton = document.getElementById("content-button");
            
            if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
                // When scrolled down past the top
                contentButton.classList.add("hidden");
            } else {
                // When at the top of the page
                contentButton.classList.remove("hidden");
            }
        }
    
        document.addEventListener("DOMContentLoaded", function () {
            const skipLinks = document.querySelectorAll('.skip-link'); // Select all skip links
            const detailsElements = document.querySelectorAll('details'); // Select all details elements

            // Function to close all details (drop-downs)
            function closeAllDetails() {
                detailsElements.forEach(details => {
                    details.removeAttribute('open'); // Close the details element
                });
            }

            // Add click event to each skip link
            skipLinks.forEach(link => {
                link.addEventListener('click', function () {
                    closeAllDetails(); // Close all details when a skip link is clicked
                });
            });
        });
        
    document.addEventListener("DOMContentLoaded", function() {
    // Select the legend items
    const legendItems = document.querySelectorAll('.legend-item'); 

    // Add click event listener to each legend item
    legendItems.forEach(item => {
        item.addEventListener('click', function() {
            // Select the corresponding icon within the clicked item
            const icon = item.querySelector('.legend-icon');

            // Add the glow effect to the icon
            icon.classList.add('glow-icon');

            // Remove the glow effect after the animation ends
            setTimeout(() => {
                icon.classList.remove('glow-icon');
            }, 600); // Duration matches the CSS animation duration
        });
    });
});
    
        // JavaScript functions for theme toggle, lightbox, progress bar, and smooth scroll
        function setTheme(theme) {
            document.body.setAttribute("data-theme", theme);
            localStorage.setItem("theme", theme);
        }

        document.addEventListener("DOMContentLoaded", function () {
            const savedTheme = localStorage.getItem("theme");
            if (savedTheme) setTheme(savedTheme);
            else setTheme(window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
        });

        function openLightbox(src) {
            document.getElementById("lightbox").style.display = "flex";
            document.getElementById("lightbox-img").src = src;
        }

        function closeLightbox() {
            document.getElementById("lightbox").style.display = "none";
        }
        
        function openLightbox(src) {
            const lightbox = document.getElementById("lightbox");
            const lightboxImg = document.getElementById("lightbox-img");
            lightboxImg.src = src;
            lightbox.style.display = "flex"; // Show the lightbox
        }

        function closeLightbox() {
            const lightbox = document.getElementById("lightbox");
            lightbox.style.display = "none"; // Hide the lightbox
        }
        
        document.addEventListener("DOMContentLoaded", function() {
        const profileImages = document.querySelectorAll("img[tabindex='0']");

        profileImages.forEach(img => {
            // Open lightbox on click
            img.addEventListener("click", function() {
                openLightbox(img.src);
            });

            // Open lightbox on Enter key
            img.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    openLightbox(img.src);
                }
            });
        });

        // Close lightbox on pressing Escape key
        document.addEventListener("keydown", function(event) {
                if (event.key === "Escape") {
                closeLightbox();
                }
            });
        });

        function toggleThemeOptions() {
            const themeOptions = document.querySelector('.theme-options');
            themeOptions.classList.toggle('active');
        }

        function scrollToSymbol(symbolClass) {
            const targetElement = document.querySelector(`.${symbolClass}`);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }

        // Progress Bar
        document.addEventListener("scroll", () => {
            const progressBar = document.getElementById("progress-bar");
            const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const progress = (scrollTop / scrollHeight) * 100;
            progressBar.style.width = progress + "%";
        });
    </script>
</body>
</html>
    '''
    
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