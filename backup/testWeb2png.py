import subprocess

def scrape_url(url, outpath):
    """
    Requires webkit2png to be on the path
    """
    subprocess.call(["webkit2png", "-o", outpath, "-g", "1000", "1260",
                     "-t", "30", url])

def scrape_list_urls(list_url_out_name, outdir):
    """
    list_url_out_name is a list of tuples: (url, name)
    where name.png will be the image's name
    """
    count = 0
    for url, name in list_url_out_name:
        print count
        count += 1
        outpath = outdir + name + '.png'
        scrape_url(url, outpath)



scrape_url("http://www.learnersdictionary.com/", "/Users/Jason/Desktop")
