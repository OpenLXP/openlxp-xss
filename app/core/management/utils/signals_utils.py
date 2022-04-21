from core.models import ChildTermSet, Term


def create_child_termset(termset_name, parent_iri):
    """function to create/save termset"""
    parent_iri = \
        ChildTermSet.objects.create(parent_term_set=parent_iri,
                                    name=termset_name)
    parent_iri.save()

    return parent_iri


def create_terms(term_obj, term_name, parent_iri):
    """function to create/save terms"""

    term = \
        Term.objects.create(term_set=parent_iri, name=term_name)
    term.__dict__.update(term_obj)
    term.save()

    return term


def save_metadata(metadata, schema_iri):
    """Function to flatten/normalize  data dictionary"""

    # Check every key elements value in data
    for element in metadata:
        # If Json Field value is a Nested Json
        if isinstance(metadata[element], dict):
            for sub_element in metadata[element]:
                if isinstance(metadata[element][sub_element], dict):
                    parent_iri = create_child_termset(element, schema_iri)
                    termset_object(metadata[element], parent_iri)
                # If Json Field value is a string
                else:
                    if isinstance(metadata[element][sub_element], str):
                        term_object(metadata[element], element, schema_iri)
                break


def termset_object(termset_obj, parent_iri):
    """function to flatten dictionary object"""

    for element in termset_obj:
        if isinstance(termset_obj[element], dict):
            for sub_element in termset_obj[element]:
                if isinstance(termset_obj[element][sub_element], dict):
                    new_parent_iri = create_child_termset(element, parent_iri)
                    termset_object(termset_obj[element], new_parent_iri)
                # If Json Field value is a string
                else:
                    if isinstance(termset_obj[element][sub_element], str):
                        term_object(termset_obj[element], element, parent_iri)
                break


def term_object(term_obj, term_name, parent_iri):
    """function to update flattened object to dict variable"""
    # new_parent_iri=create a term(parent_iri)

    create_terms(term_obj, term_name, parent_iri)
