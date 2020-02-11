#!/usr/bin/env python
from annette.stages.harvest import HarvestCore
from annette.stages.identify import IdentifyCore
from annette.models import Session, RunLogManager

# Open new db session
session = Session()

with RunLogManager(session) as logger:
    # HARVEST STAGE
    extracted_citations = HarvestCore.run()
    HarvestCore.store(session, extracted_citations)
    logger.complete('harvest')

    # IDENTIFY STAGE
    citations = IdentifyCore.run()
    IdentifyCore.store(session, citations)
    logger.complete('identify')

    # old code -------------------------------------------------------------------------------------
    # # Set cutoff to one month before current date
    # cutoff = date.today() - timedelta(days=31)
    #
    # # Query extractedcitation_store for records which haven't been checked against crossref
    # # in the last month (or ever)
    # mystery_extractedcitations = list(session.query(ExtractedCitation)
    #                                   .filter(or_(ExtractedCitation.last_identify_run is None,
    #                                               ExtractedCitation.last_identify_run < cutoff))
    #                                   .filter(not ExtractedCitation.id_status).limit(50))
    #
    # # Get bib data from crossref and update extractedcitations with confirmed DOI
    # identified_citations, id_extractedcitations = IdentifyCrossRef(
    #     mystery_extractedcitations).get_crossref_match()
    #
    # # Update extractedcitation table for both matched and unmatched extractedcitations
    # session.add_all(id_extractedcitations)
    #
    # # Get all known citations
    # known_citations = {x.doi for x in session.query(Citation)}
    #
    # # Strip out citations already in the database
    # identified_citations = [d for d in identified_citations if d.doi not in known_citations]
    #
    # # Add new citations
    # session.add_all(identified_citations)
    # logging.info(f"{len(identified_citations)} citations written to citation_store.")
    # session.flush()
    # print("crossref identifications written to db")
    # ----------------------------------------------------------------------------------------------

    # ENHANCE STAGE

    logger.complete('enhance')

    # ----------------------------------------------------------------------------------------------
    # # Harvest metrics monthly
    # if date.today().day == 1:
    #     logging.info("Running metrics...")
    #     citation_dois = list(session.query(Citation).filter(Citation.classification_id == True))
    #     session.flush()
    #
    #     new_metrics = Dimensions(citation_dois).get_citations()
    #
    #     # Write to bibliometrics table and log results
    #     session.add_all(new_metrics)
    #     logging.info(f"{len(new_metrics)} access metrics written to bibliometrics.")
    #     session.flush()
    #
    # print("starting access queries")
    # # Get access data for citations newly-identified in this pass
    # new_access = Unpaywall(identified_citations).get_access_data()
    # session.add_all(new_access)
    # session.flush()
    #
    # # Every six months, re-check all Citation records for updated access info
    # if date.today().day == 1 and (date.today().month == 12 or date.today().month == 6):
    #
    #     all_records = list(session.query(Citation)
    #                        .filter(Citation.classification_id == True,
    #                                Citation.identified_date != date.today()))
    #
    #     updated_access_records = Unpaywall(all_records).get_access_data()
    #     session.add_all(updated_access_records)
    #     session.flush()
    #
    # unclassified_citations = list(
    #     session.query(Citation).filter(Citation.classification_id == None))
    # print("finished access queries - starting classification")
    # ----------------------------------------------------------------------------------------------

    # CLASSIFY STAGE

    logger.complete('classify')

    # ----------------------------------------------------------------------------------------------
    # if unclassified_citations:
    #     classified_citations = Classifier(unclassified_citations).classify()
    #     session.add_all(classified_citations)
    #     session.flush()
    #
    # print("classification finished starting name parsing...")
    #
    # # Extract taxonomic names (Limited to new papers)
    # nhm_citations = list(session.query(Citation)
    #     .filter(Citation.identified_date == date.today())
    #     .filter(
    #     or_(Citation.type == 'peer-review', Citation.type == 'journal-article')))
    #
    # # Get names for each title
    # result = []
    # for x in nhm_citations:
    #     result.extend(FindNames(x.doi, x.title).get_names())
    #
    # # Convert each sp. name into a Name object + write to db
    # names = [Name(doi=r[0], label=r[1], rundate=date.today()) for r in result]
    # session.add_all(names)
    # session.flush()
    #
    # # Get distinct usage key values already in Taxonomy table
    # taxonomy_keys = list(chain.from_iterable(session.query(Taxonomy.usageKey.distinct())))
    #
    # # Retrieve names in need of resolution
    # unresolved_names = list(session.query(Name).filter(Name.usage_key == None))
    #
    # #  Match names against gbif backbone
    # res_names, updated_names = ResolveName(unresolved_names).gbif_name_resolve()
    #
    # distinct_results = []
    #
    # # Get rid of duplicates
    # for n in res_names:
    #     if n.usageKey not in taxonomy_keys:
    #         distinct_results.append(n)
    #         taxonomy_keys.append(n.usageKey)
    #
    # session.add_all(updated_names)
    # session.flush()
    #
    # session.add_all(distinct_results)
    # session.flush()
    #
    # print(f"{len(distinct_results)} added to taxonomy table")
    # ----------------------------------------------------------------------------------------------

