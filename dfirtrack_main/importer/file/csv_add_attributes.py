from dfirtrack_main.models import Case, Company, Dnsname, Domain, Location, Ip, Os, Reason, Recommendation, Serviceprovider, Systemtype, Tag, Tagcolor

def add_fk_attributes(system, system_created, model, row):
    """ add foreign key relationships to system """

    """ systemstatus """

    # set systemstatus for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_systemstatus):

        # set systemstatus for system
        system.systemstatus = model.csv_default_systemstatus

    """ analysisstatus """

    # set analysisstatus for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_analysisstatus):

        # set analysisstatus for system
        system.analysisstatus = model.csv_default_analysisstatus

# TODO: add checks for content of 'csv_column_...'
# TODO: do something like: 'try: ...get_or_create(...)'

# TODO: not forget the logger and / or message

    """ dnsname """

    # set dnsname for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_dnsname):
        # get dnsname from CSV
        if model.csv_choice_dnsname:
            # get dnsname from CSV column
            dnsname_name = row[model.csv_column_dnsname - 1]
            # check for empty string
            if dnsname_name:
                # get or create dnsname
                dnsname, created = Dnsname.objects.get_or_create(dnsname_name = dnsname_name)
                # call logger if created
                if created:
                    dnsname.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_DNSNAME_CREATED")
            else:
                # set empty value (field is empty)
                dnsname = None
        # get dnsname from DB
        elif model.csv_default_dnsname:
            dnsname = model.csv_default_dnsname
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            dnsname = None
        # set dnsname for system
        system.dnsname = dnsname

    """ domain """

    # set domain for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_domain):
        # get domain from CSV
        if model.csv_choice_domain:
            # get domain from CSV column
            domain_name = row[model.csv_column_domain - 1]
            # check for empty string and compare to system name (when queried with local account, hostname is returned under some circumstances depending on tool)
            if domain_name and domain_name != system.system_name:
                # get or create domain
                domain, created = Domain.objects.get_or_create(domain_name = domain_name)
                # call logger if created
                if created:
                    domain.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_DOMAIN_CREATED")
            else:
                # set empty value (field is empty)
                domain = None
        # get domain from DB
        elif model.csv_default_domain:
            domain = model.csv_default_domain
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            domain = None
        # set domain for system
        system.domain = domain

    """ location """

    # set location for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_location):
        # get location from CSV
        if model.csv_choice_location:
            # get location from CSV column
            location_name = row[model.csv_column_location - 1]
            # check for empty string
            if location_name:
                # get or create location
                location, created = Location.objects.get_or_create(location_name = location_name)
                # call logger if created
                if created:
                    location.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_LOCATION_CREATED")
            else:
                # set empty value (field is empty)
                location = None
        # get location from DB
        elif model.csv_default_location:
            location = model.csv_default_location
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            location = None
        # set location for system
        system.location = location

    """ os """

    # set os for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_os):
        # get os from CSV
        if model.csv_choice_os:
            # get os from CSV column
            os_name = row[model.csv_column_os - 1]
            # check for empty string
            if os_name:
                # get or create os
                os, created = Os.objects.get_or_create(os_name = os_name)
                # call logger if created
                if created:
                    os.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_OS_CREATED")
            else:
                # set empty value (field is empty)
                os = None
        # get os from DB
        elif model.csv_default_os:
            os = model.csv_default_os
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            os = None
        # set os for system
        system.os = os

    """ reason """

    # set reason for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_reason):
        # get reason from CSV
        if model.csv_choice_reason:
            # get reason from CSV column
            reason_name = row[model.csv_column_reason - 1]
            # check for empty string
            if reason_name:
                # get or create reason
                reason, created = Reason.objects.get_or_create(reason_name = reason_name)
                # call logger if created
                if created:
                    reason.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_REASON_CREATED")
            else:
                # set empty value (field is empty)
                reason = None
        # get reason from DB
        elif model.csv_default_reason:
            reason = model.csv_default_reason
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            reason = None
        # set reason for system
        system.reason = reason

    """ recommendation """

    # set recommendation for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_recommendation):
        # get recommendation from CSV
        if model.csv_choice_recommendation:
            # get recommendation from CSV column
            recommendation_name = row[model.csv_column_recommendation - 1]
            # check for empty string
            if recommendation_name:
                # get or create recommendation
                recommendation, created = Recommendation.objects.get_or_create(recommendation_name = recommendation_name)
                # call logger if created
                if created:
                    recommendation.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_RECOMMENDATION_CREATED")
            else:
                # set empty value (field is empty)
                recommendation = None
        # get recommendation from DB
        elif model.csv_default_recommendation:
            recommendation = model.csv_default_recommendation
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            recommendation = None
        # set recommendation for system
        system.recommendation = recommendation

    """ serviceprovider """

    # set serviceprovider for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_serviceprovider):
        # get serviceprovider from CSV
        if model.csv_choice_serviceprovider:
            # get serviceprovider from CSV column
            serviceprovider_name = row[model.csv_column_serviceprovider - 1]
            # check for empty string
            if serviceprovider_name:
                # get or create serviceprovider
                serviceprovider, created = Serviceprovider.objects.get_or_create(serviceprovider_name = serviceprovider_name)
                # call logger if created
                if created:
                    serviceprovider.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_SERVICEPROVIDER_CREATED")
            else:
                # set empty value (field is empty)
                serviceprovider = None
        # get serviceprovider from DB
        elif model.csv_default_serviceprovider:
            serviceprovider = model.csv_default_serviceprovider
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            serviceprovider = None
        # set serviceprovider for system
        system.serviceprovider = serviceprovider

    """ systemtype """

    # set systemtype for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_systemtype):
        # get systemtype from CSV
        if model.csv_choice_systemtype:
            # get systemtype from CSV column
            systemtype_name = row[model.csv_column_systemtype - 1]
            # check for empty string
            if systemtype_name:
                # get or create systemtype
                systemtype, created = Systemtype.objects.get_or_create(systemtype_name = systemtype_name)
                # call logger if created
                if created:
                    systemtype.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_SYSTEMTYPE_CREATED")
            else:
                # set empty value (field is empty)
                systemtype = None
        # get systemtype from DB
        elif model.csv_default_systemtype:
            systemtype = model.csv_default_systemtype
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            systemtype = None
        # set systemtype for system
        system.systemtype = systemtype

    # return system with foreign key relations
    return system

def add_many2many_attributes(system, system_created, model, row):
    """ add many2many relationships to system """

    """ IP addresses """

# TODO: add check for IP (used somewhere else)

    # add ips for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_ip):
        # remove ips if not new system
        if not system_created:
            # remove all IPs
            system.ip.clear()
        # get IPs from CSV
        if model.csv_choice_ip:
            # get ip string
            ip_string = row[model.csv_column_ip - 1]
            # check for empty string
            if ip_string:
                # get IP delimiter from config
                if model.csv_ip_delimiter == 'ip_comma':
                    ip_delimiter = ','
                elif model.csv_ip_delimiter == 'ip_semicolon':
                    ip_delimiter = ';'
                elif model.csv_ip_delimiter == 'ip_space':
                    ip_delimiter = ' '
                # split ip string to list depending on delimiter
                ip_list = ip_string.split(ip_delimiter)
                # iterate over list elements
                for ip_ip in ip_list:
                    # get or create ip
                    ip, created = Ip.objects.get_or_create(ip_ip = ip_ip)
                    # call logger if created
                    if created:
                        ip.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_IP_CREATED")
                    # add ip to system
                    system.ip.add(ip)

    """ case """

    # set case for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_case):
        # remove cases if not new system
        if not system_created:
            # remove all cases
            system.case.clear()
        # get case from CSV
        if model.csv_choice_case:
            # get case from CSV column
            case_name = row[model.csv_column_case - 1]
            # check for empty string
            if case_name:
                # get case
                try:
                    case = Case.objects.get(
                        case_name = case_name,
                    )
                # create case
                except Case.DoesNotExist:
                    case, created = Case.objects.get_or_create(
                        case_name = case_name,
                        case_is_incident = False,
                        case_created_by_user_id = model.csv_import_username,
                    )
                    # call logger if created
                    if created:
                        case.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_CASE_CREATED")
                # set case for system
                system.case.add(case)
        # get case from DB
        elif model.csv_default_case:
            cases = model.csv_default_case
            for case in cases.all():
                # add case to system
                system.case.add(case)

    """ company """

    # set company for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_company):
        # remove companies if not new system
        if not system_created:
            # remove all companies
            system.company.clear()
        # get company from CSV
        if model.csv_choice_company:
            # get company from CSV column
            company_name = row[model.csv_column_company - 1]
            # check for empty string
            if company_name:
                # get or create company
                company, created = Company.objects.get_or_create(company_name = company_name)
                # call logger if created
                if created:
                    company.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_COMPANY_CREATED")
                # set company for system
                system.company.add(company)
        # get company from DB
        elif model.csv_default_company:
            companys = model.csv_default_company
            for company in companys.all():
                # add company to system
                system.company.add(company)

    """ tag """

    # set tag for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_tag != 'tag_remove_none'):

        """ prepare tag prefix """

        # get tag delimiter from config
        if model.csv_tag_prefix_delimiter == 'tag_prefix_underscore':
            tag_prefix_delimiter = '_'
        elif model.csv_tag_prefix_delimiter == 'tag_prefix_hyphen':
            tag_prefix_delimiter = '-'
        elif model.csv_tag_prefix_delimiter == 'tag_prefix_period':
            tag_prefix_delimiter = '.'

        # build tagprefix string from prefix and delimiter
        tagprefix = model.csv_tag_prefix + tag_prefix_delimiter

        """ remove tags for existing systems (either all or just with prefix) """

        # remove all tags
        if not system_created and model.csv_remove_tag == 'tag_remove_all':
            # remove all tags
            system.tag.clear()

        # remove tags with prefix (and keep other / manually set tags)
        elif not system_created and model.csv_remove_tag == 'tag_remove_prefix':
            # get all relevant tags for this system
            prefixtags = system.tag.filter(tag_name__startswith=tagprefix)
            # iterate over tags
            for prefixtag in prefixtags:
                # remove this tag relation from system
                prefixtag.system_set.remove(system)

        """ add tags from CSV or DB """

        # get tags from CSV
        if model.csv_choice_tag:
            # get tagstring from CSV column
            tag_string = row[model.csv_column_tag - 1]

            # check for empty string
            if tag_string:

                # get tag delimiter from config
                if model.csv_tag_delimiter == 'tag_comma':
                    tag_delimiter = ','
                elif model.csv_tag_delimiter == 'tag_semicolon':
                    tag_delimiter = ';'
                elif model.csv_tag_delimiter == 'tag_space':
                    tag_delimiter = ' '
                # split tag string to list depending on delimiter
                tag_list = tag_string.split(tag_delimiter)

                # get tagcolor
                tagcolor_primary = Tagcolor.objects.get(tagcolor_name='primary')
                # iterate over tags
                for tag in tag_list:
                    # build tagname from prefix, prefix delimiter and name
                    tagname = tagprefix + tag
                    # get tag
                    try:
                        tag = Tag.objects.get(
                            tag_name = tagname,
                        )
                    # create tag
                    except Tag.DoesNotExist:
                        tag, created = Tag.objects.get_or_create(
                            tag_name = tagname,
                            tagcolor = tagcolor_primary,
                        )
                        # call logger if created
                        if created:
                            tag.logger(model.csv_import_username.username, " SYSTEM_IMPORTER_FILE_CSV_CRON_TAG_CREATED")
                    # add tag to system
                    system.tag.add(tag)

        # get tags from DB
        elif model.csv_default_tag:
            tags = model.csv_default_tag
            for tag in tags.all():
                # add tag to system
                system.tag.add(tag)

    # return system with many2many relations
    return system