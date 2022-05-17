from core.models import ChildTermSet, Term


def create_child_termset(termset_name, parent_iri, status, updated_by):
    """function to create/save termset"""
    parent_iri = \
        ChildTermSet.objects.create(parent_term_set=parent_iri,
                                    name=termset_name,
                                    status=status,
                                    updated_by=updated_by)
    parent_iri.save()

    return parent_iri


def create_terms(term_obj, term_name, parent_iri, status, updated_by):
    """function to create/save terms"""

    term = \
        Term.objects.create(term_set=parent_iri, name=term_name,
                            status=status, updated_by=updated_by)
    term.__dict__.update(term_obj)
    term.save()

    return term


def termset_object(metadata, schema_iri, status, updated_by):
    """Function to flatten/normalize data dictionary"""

    # Check every key elements value in data
    for element in metadata:
        # If Json Field value is a Nested Json
        if isinstance(metadata[element], dict):
            for sub_element in metadata[element]:
                if isinstance(metadata[element][sub_element], dict):
                    parent_iri = create_child_termset(
                        element, schema_iri, status, updated_by)
                    termset_object(metadata[element], parent_iri, status,
                                   updated_by)
                # If Json Field value is a string
                elif isinstance(metadata[element][sub_element], str):
                    term_object(
                        metadata[element], element, schema_iri, status,
                        updated_by)
                break


def term_object(term_obj, term_name, parent_iri, status, updated_by):
    """function to update flattened object to dict variable"""

    create_terms(term_obj, term_name, parent_iri, status, updated_by)


def update_status(termset, status, updated_by):
    """function to update the status of children terms/termsets"""

    child_termset = ChildTermSet.objects.filter(parent_term_set=termset)

    if child_termset:
        for child_element in child_termset:
            child_termset.update(status=status, updated_by=updated_by)
            update_status(child_element, status, updated_by)

    term = termset.terms
    term.update(status=status, updated_by=updated_by)
