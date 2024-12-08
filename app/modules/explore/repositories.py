import re
from sqlalchemy import case, or_
import unidecode
from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter(self, query="", sorting="newest", publication_type="any", tags=[], **kwargs):
        # Normalize and clean query string
        normalized_query = unidecode.unidecode(query).strip()

        filters = []

        # Parse field-specific queries
        field_pattern = re.compile(r'(\w+):"([^"]+)"')  # Matches `field:"value"`
        field_matches = field_pattern.findall(normalized_query)
        if field_matches:
            for field, value in field_matches:
                value = value.strip()  # Clean value
                if field == "title":
                    filters.append(DSMetaData.title.ilike(f"%{value}%"))
                elif field == "description":
                    filters.append(DSMetaData.description.ilike(f"%{value}%"))
                elif field == "author":
                    filters.append(Author.name.ilike(f"%{value}%"))
                elif field == "affiliation":
                    filters.append(Author.affiliation.ilike(f"%{value}%"))
                elif field == "orcid":
                    filters.append(Author.orcid.ilike(f"%{value}%"))
                elif field == "uvl_filename":
                    filters.append(FMMetaData.uvl_filename.ilike(f"%{value}%"))
                elif field == "fm_title":
                    filters.append(FMMetaData.title.ilike(f"%{value}%"))
                elif field == "fm_description":
                    filters.append(FMMetaData.description.ilike(f"%{value}%"))
                elif field == "publication_doi":
                    filters.append(FMMetaData.publication_doi.ilike(f"%{value}%"))
                elif field == "tags":
                    filters.append(DSMetaData.tags.ilike(f"%{value}%"))
        else:
            # General text search
            cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query).lower()
            for word in cleaned_query.split():
                filters.extend([
                    DSMetaData.title.ilike(f"%{word}%"),
                    DSMetaData.description.ilike(f"%{word}%"),
                    Author.name.ilike(f"%{word}%"),
                    Author.affiliation.ilike(f"%{word}%"),
                    Author.orcid.ilike(f"%{word}%"),
                    FMMetaData.uvl_filename.ilike(f"%{word}%"),
                    FMMetaData.title.ilike(f"%{word}%"),
                    FMMetaData.description.ilike(f"%{word}%"),
                    FMMetaData.publication_doi.ilike(f"%{word}%"),
                    FMMetaData.tags.ilike(f"%{word}%"),
                    DSMetaData.tags.ilike(f"%{word}%"),
                ])

        # Base query
        datasets = (
            self.model.query
            .join(DataSet.ds_meta_data, isouter=True)
            .join(DSMetaData.authors, isouter=True)
            .join(DataSet.feature_models, isouter=True)
            .join(FeatureModel.fm_meta_data, isouter=True)
            .filter(or_(*filters))  # Apply text search filters
            .filter(DSMetaData.dataset_doi.isnot(None))  # Exclude datasets without DOI
        )

        # Filter by publication type
        if publication_type != "any":
            matching_type = next((pt for pt in PublicationType if pt.value.lower() == publication_type), None)
            if matching_type:
                datasets = datasets.filter(DSMetaData.publication_type == matching_type.name)

        # Filter by tags
        if tags:
            datasets = datasets.filter(
                or_(*(DSMetaData.tags.ilike(f"%{tag}%") for tag in tags))
            )

        # Sorting (MySQL/MariaDB-compatible)
        if sorting == "oldest":
            datasets = datasets.order_by(
                case(
                    (self.model.created_at.is_(None), 1),
                    else_=0
                ),  # Treat NULLs as larger for oldest sorting
                self.model.created_at.asc()
            )
        else:
            datasets = datasets.order_by(
                case(
                    (self.model.created_at.is_(None), 1),
                    else_=0
                ),  # Treat NULLs as larger for newest sorting
                self.model.created_at.desc()
            )

        return datasets.all()
