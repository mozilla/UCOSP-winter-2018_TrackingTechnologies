import pandas as pd


def make_entity_list_df():
    """Create df from disconnectme entity list."""
    frames = []
    entityList = pd.read_json(
        "https://raw.githubusercontent.com/disconnectme/disconnect-tracking-protection/master/services.json")

    for category in entityList["categories"]:  # Category eg. "Advertising"
        for entity in category:  # Entity eg. {'reddit': {'http://www.reddit.com/': ['reddit.com']}}
            name = list(entity.keys())[0]
            url = list(entity[name].keys())[0]

            # Rename key from original url to "resources" to collapse resulting df columns.
            entity[name]["resources"] = entity[name][url]
            del entity[name][url]

            # Create df for each entity.
            frame = pd.DataFrame.from_dict(entity, orient="index")
            frames.append(frame)

    result = pd.concat(frames)
    result["count"] = 0
    return result[["resources", "count"]]


def sample_random_files(files):
    """Produce statistics for subset of files
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

    # For each unique call, for every site owned by a domain on the entity list,
    # increment count for that domain if the call uses a script from a site owned by the domain.
    for i, rowCalls in uniquecalls.iterrows():
        match_found = False
        url = rowCalls["script_url"]
        if "//" in url:
            # Isolate the TLD+1 element by string matching between "//" and first occurrence of "/" element.
            url = url.split("//")[1].split("/")[0]
        else:
            print("irregular script_url: ", url)
        # TODO: This deeply nested loop can be made more efficient.
        # TODO: Add comments inside lop to explain the flow of execution.
        for j, rowResult in result.iterrows():
            if not match_found:
                for site in result["sites"][j]:
                    if not match_found:
                        if site in url:
                            if not result.at[j, "calledFrom"]:
                                result.at[j, "calledFrom"] = []
                            result.at[j, "calledFrom"].append(rowCalls["location"])
                            result.at[j, 'count'] += 1
                            print("match found! ", "script_url: ", site, "calledFrom: ", url)
                            match_found = True
                    else:
                        # Match found already.
                        break

    return result[result['count'] > 0]


el = make_entity_list_df()
