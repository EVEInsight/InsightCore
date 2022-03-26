class Filters(object):
    @classmethod
    def filter_ids(cls, filter_ids_include, filter_ids_exclude, mail_id) -> bool:
        """Checks if the ID from a mail exists in filter_ids_include after removing filter_ids_exclude

        :param filter_ids_include: The match filter ids of integers. Can include the "*" wildcard string to match all.
        :type filter_ids_include: list[int]
        :param filter_ids_exclude: The excluded filter ids of integers.
        :type filter_ids_exclude: list[int]
        :param mail_id: The comparison id that must exist in set(filter_ids_include) - set(filter_ids_exclude)
        :return: True if mail_id exists in set(filter_ids_include) - set(filter_ids_exclude) else False
        """
        set_filter_ids_include = set(filter_ids_include)
        set_filter_ids_exclude = set(filter_ids_exclude)
        filter_ids = set_filter_ids_include - set_filter_ids_exclude
        if "*" in set_filter_ids_include and mail_id not in set_filter_ids_exclude:
            return True
        elif "*" in set_filter_ids_include and mail_id in set_filter_ids_exclude:
            return False
        elif mail_id in filter_ids:
            return True
        else:
            return False
