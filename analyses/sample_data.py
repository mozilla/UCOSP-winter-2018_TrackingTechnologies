import pandas as pd
import tldextract

def make_entity_list_df():
    """Create df from disconnectme entity list."""
    frames = []
    entityList = pd.read_json(
        "https://raw.githubusercontent.com/disconnectme/disconnect-tracking-protection/master/services.json")
    
    for category in entityList["categories"]:   # Category eg. "Advertising"
        for entity in category:                 # Entity eg. {'reddit': {'http://www.reddit.com/': ['reddit.com']}} 
            name = list(entity.keys())[0]
            url = list(entity[name].keys())[0]

            # Rename key from original url to "resources" to collapse resulting df columns.
            entity[name]["resources"] = entity[name][url]
            del entity[name][url]

            # Create df for each entity.
            frame = pd.DataFrame.from_dict(entity, orient="index")
            frames.append(frame)

    result = pd.concat(frames)

    # Group rows by entity name.
    result = result.groupby(result.index,sort=True).sum()

    result["count"] = 0

    # Output df example row: LinkedIn [licdn.com, linkedin.com]  0
    return result[["resources", "count"]]

def find_url_match(script_url, entity_site):
    if "//" in script_url:
        # Get top level domains for script_url and entity website.
        url_domain = tldextract.extract(script_url).domain
        site_domain = tldextract.extract(entity_site).domain

        if url_domain == site_domain:
            return True
        else:
            return False
    else:
        print("irregular script_url: ", script_url)
        return "IrregularUrl"

def sample_random_files(files):
    """Produce script_url statistics for subset of files
    Specifically, for each unique script call, for every TDL domain on the entity list,
    increment count for that domain if it owns the called script.

    Keyword arguments:
    files -- df of random files produced by load_random_data()

    Output: 
    df containing TDL's with count > 0, where count represents the number of times 
    a script was called from a site belonging to that TDL
    """

    result = make_entity_list_df()

    # Remove rows where one TDL calls the same script url (ie. only keep unique calls).
    uniquecalls = files.drop_duplicates(subset={'location', 'script_url'}, keep="last")

    # Reset samplings statistics.
    result["count"] = 0
    result["calledFrom"] = [[]] * len(result)
    result["usesCryptojacking"] = False

    # Iterate through unique script calls, pull script urls.
    for i, rowCalls in uniquecalls.iterrows():
        match_found = False
        url = rowCalls["script_url"]

        # Iterate through each TLD entity and its owned resources/websites.
        for j, rowResult in result.iterrows():
            if match_found == False:
                # Determine if the called script is owned by the TLD entity.
                for site in rowResult["resources"]:
                    match_found = find_url_match(url, site)
                    if match_found == True:
                        # Initiate calledFrom column as empty list if it does not contain a calledFrom location.
                        if not result.at[j, "calledFrom"]:
                            result.at[j, "calledFrom"] = []

                        # Store url of location that is calling the script.
                        result.at[j, "calledFrom"].append(rowCalls["location"])

                        # Check if cryptojacking services from CoinHive or Crypto-Loot are being used.
                        if rowResult.name == "CoinHive" or  rowResult.name == "Crypto-Loot":
                            result.at[j, "usesCryptojacking"] = True

                        # TDL owns the script; increment count.
                        result.at[j,'count'] += 1

                        print("match found! ", "script_url:", url, "domain:", site)
                        # Match found, not necessary to continue comparing urls.
                        break

                    elif match_found == "IrregularUrl":
                        # Not possible to find match for irregular url, break loop.
                        break

            else:
                # Match found already.
                break

    return result[result['count'] > 0]
