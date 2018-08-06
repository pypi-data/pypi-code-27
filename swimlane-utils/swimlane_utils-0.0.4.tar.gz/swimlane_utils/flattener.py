# Basic Flattening Utility
# Author: Spencer Hanson, for Swimlane!


# Mixin to easily call flatten funcs
class FlattenMixin(object):
    # Hoist out a specific key within a given listdict
    # Ex: hoist_key("a", [{"a": 1, "b": 4},{"a": 2}, ..]) ->
    # [1,2,3]
    def hoist_key(self, key, from_list):
        hoisted = []
        for element in from_list:
            if key not in element:
                raise Exception("Key {} not found in dict {}".format(key, element))
            hoisted.append(element[key])
        return hoisted

    # Hoist out a specific keys within a given listdict
    # Ex: hoist_keys(["a", "b"], [{"a": 1, "b": 4},{"a": 2, "b": 2, "c": 3}, ..]) ->
    # [[all a keys], [all b keys]] -> [[1,2],[4,2]]
    def hoist_keys(self, key_list, from_list):
        hoisted = []
        for key in key_list:
            hoisted.append(self.hoist_key(key, from_list))
        return hoisted

    # Change a similar prefix on keys within a dict to something else, say 'annoying_stuff_' -> 'a_'
    # Ex {"annoying_stuff_important_stuff": "data", "annoying_stuff_asdf": "data2"} ->
    # {"a_important_stuff": "data", "a_asdf": "data2"}
    def replace_dict_prefix(self, prefix, replace_val, from_dict):
        for k in from_dict.keys():
            if k.startswith(prefix):
                newk = k.replace(prefix, replace_val)
                if newk in from_dict:
                    raise Exception("Can't remove prefix, results in namespace collision!")
                from_dict[newk] = from_dict.pop(k)
        return from_dict

    # Squish dict with keys with keyname and valuename such that if
    # from_dict = {a: b, c: d}
    # keyname = "keynames"
    # valname = "valnames"
    # Then -> to_dict = {keynames: [a,c], valnames: [b,d]}
    def squish_dict(self, from_dict, to_dict, keyname, valuename):
        to_dict[keyname] = list(from_dict.keys())
        to_dict[valuename] = list(from_dict.values())
        return to_dict

    # Map keys from the listdict into the outer dict, given a mapping
    # Ex remap_flatten_listdict([{a: 1, g: 88},{a: 2},{a: 3}], {}, {a: b}) ->
    # {b: [1,2,3]}
    #
    # This does NOT work with recursively, and only remaps the firstmost keys
    def remap_flatten_listdict(self, from_list, to_dict, mapping):
        if not len(from_list) > 0:
            return to_dict

        for item in from_list:
            for oldk in item.keys():
                if not mapping[oldk]:
                    # Skip this mapping
                    continue
                if not mapping[oldk] in to_dict:
                    to_dict[mapping[oldk]] = []
                to_dict[mapping[oldk]].append(item[oldk])
        return to_dict

    # Mapping to change the name of inner keys, while flattening the inner keys
    # Ex: a['scan_results'] = {"AV#1": {"threat_found": ...}, "AV#2": {..}, ... } goes to
    # a['av_threat_found'] = [<threat_found_1>, <threat_found_2>, ...]
    # where mapping = {"old_key": "new_key", ...}
    # and keyname_mapping is the key in 'to_dict' to store a list of the keynames from the listdict
    #
    # This does NOT work with recursively, and only remaps the firstmost keys
    def remap_flatten_dict(self, from_dict, to_dict, mapping, keyname_mapping=None):
        # Add a new list for the new keys
        if keyname_mapping:
            to_dict[keyname_mapping] = []
        for old_name, new_name in mapping.iteritems():
            to_dict[new_name] = []

        # Go through all mappings, add them to the data
        for from_k, from_v in from_dict.iteritems():
            for old_name, new_name in mapping.iteritems():  # Map values into the new dict
                to_dict[new_name].append(from_v[old_name])
            if keyname_mapping:  # If we're keeping track of they keys add it
                to_dict[keyname_mapping].append(from_k)
        return to_dict

    # Map keys from 'from_data' to 'to_data' using a mapping
    # will overwrite with collisions
    # 'mapping' can be a dict like {key1: val1, key2: val2}
    # or a function with expected signature func(key, val) and returns the new key
    def remap_keys(self, from_data, to_data, mapping):
        if isinstance(mapping, dict):
            for k, v in mapping.iteritems():
                to_data[v] = from_data[k]
        elif callable(mapping):
            for k, v in from_data.iteritems():
                k1 = mapping(k, v)
                to_data[k1] = from_data[k]
        else:
            raise Exception("Invalid mapping given, use dict or function")
        return to_data

    # Helper method for flatten_data, used to help flatten recursive list-dicts
    # Takes the data of the dict to store the flattened output like {"a": "val1", "b": ...}
    # And the value of the subdict with similar keys, like {"a": "val2"}
    # Merges the two into a list {"a": ["val1", "val2"], "b": ...}
    def merge_listdict(self, data, subdict_data):
        data_keys = data.keys()
        sub_keys = subdict_data.keys()
        for key in set(data_keys).intersection(sub_keys):  # Keys that they share
            if isinstance(data[key], list):  # Already a list of this object
                data[key].append(subdict_data[key])
            else:  # It isn't a list, so to merge it we must make it into one
                data[key] = [data[key], subdict_data[key]]
        return data

    # General flattening function
    # Method to flatten a dict like
    # a["b C.D"] = {"e": f} -> a["b_cd_e"] = f
    # a["b C.D"] = [{"e": f_0, "g": h_0, ..}, {"e": f_1, "g": h_1, ..}] ->
    #                       a["b_cd_e"] =  "f0, f1, ..."
    #                       a["b_cd_g"] = " h0, h1, ..."
    # All values are basic types of string or integer
    # lists will be flattened into CSV strings
    # Works recursively on list-dicts and inner dicts
    # Also makes the keys lowercase, removes .'s and replaces spaces with underscores
    def flatten_data(self, data, prefix=None):
        flat_dict = {}
        for k, v in data.iteritems():
            k = k.replace('.', '').replace(' ', '_')  # Reformat the key
            k = prefix + "_" + k if prefix else k

            if isinstance(v, dict):  # Dict within dict
                sub_dict = self.flatten_data(v, prefix=k)
                flat_dict.update(sub_dict)
            elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):  # Current data is a list of dicts
                list_dict_keys = v[0].keys()  # This assumes that all the dicts in the list have the same schema

                # Create empty list entry for inner dict list key
                for list_dict_key in list_dict_keys:
                    flat_dict[k + "_" + list_dict_key] = []

                # Add items to flattened dict
                for item in v:
                    sub_dict = self.flatten_data(item, prefix=k)
                    flat_dict = self.merge_listdict(flat_dict, sub_dict)

                # Flatten list entries within dict
                for list_dict_key in list_dict_keys:
                    flat_dict[k + "_" + list_dict_key] = \
                        ",".join(unicode(entry) for entry in flat_dict.get(k + "_" + list_dict_key))

            elif isinstance(v, list):  # Normal list
                flat_dict[k] = ",".join(unicode(vi) for vi in v)
            else:  # Base case, unflattenable value
                flat_dict[k] = v
        return flat_dict
