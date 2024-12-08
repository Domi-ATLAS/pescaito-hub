import re
from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import aliased
from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter(self, query="", sorting="newest", publication_type="any", tags=[], **kwargs):
        normalized_query = query.strip()

        def create_field_condition(field, value):
            if field == "title":
                return DSMetaData.title.ilike(f"%{value}%")
            elif field == "description":
                return DSMetaData.description.ilike(f"%{value}%")
            elif field == "author":
                return Author.name.ilike(f"%{value}%")
            elif field == "tags":
                return DSMetaData.tags.ilike(f"%{value}%")
            return None

        def parse_query(query):
            query = query.replace("&&", " AND ").replace("||", " OR ").replace("!", " NOT ")
            tokens = re.split(r'(\bAND\b|\bOR\b|\bNOT\b)', query, flags=re.IGNORECASE)
            conditions = []
            current_op = None

            for token in tokens:
                token = token.strip()
                if token.upper() in ("AND", "OR", "NOT"):
                    current_op = token.upper()
                elif ":" in token:
                    field, value = token.split(":", 1)
                    field_condition = create_field_condition(field, value.strip('"'))
                    if field_condition is not None:
                        conditions.append((current_op, field_condition))
                elif token:
                    conditions.append((
                        current_op,
                        or_(
                            DSMetaData.title.ilike(f"%{token}%"),
                            DSMetaData.description.ilike(f"%{token}%"),
                            Author.name.ilike(f"%{token}%"),
                            FMMetaData.title.ilike(f"%{token}%"),
                        )
                    ))

            final_condition = None
            for op, condition in conditions:
                if final_condition is None:
                    final_condition = condition
                elif op == "AND":
                    final_condition = and_(final_condition, condition)
                elif op == "OR":
                    final_condition = or_(final_condition, condition)
                elif op == "NOT":
                    final_condition = and_(final_condition, not_(condition))

            return final_condition

        filter_condition = parse_query(normalized_query)

        if filter_condition is None:
            filter_condition = True

        datasets = (
            self.model.query
            .join(DataSet.ds_meta_data)
            .join(DSMetaData.authors)
            .join(DataSet.feature_models)
            .join(FeatureModel.fm_meta_data)
            .filter(filter_condition)
            .filter(DSMetaData.dataset_doi.isnot(None))
        )


        if publication_type != "any":
            datasets = datasets.filter(DSMetaData.publication_type.ilike(publication_type))


        if tags:
            datasets = datasets.filter(
                or_(*(DSMetaData.tags.ilike(f"%{tag}%") for tag in tags))
            )


        if sorting == "oldest":
            datasets = datasets.order_by(self.model.created_at.asc())
        else:
            datasets = datasets.order_by(self.model.created_at.desc())

        return datasets.all()
