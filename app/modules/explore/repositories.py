import re
from sqlalchemy import any_, or_
import unidecode
from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter(self, query="", sorting="newest", publication_type="any", tags=[], **kwargs):
        # Normalize and remove unwanted characters
        normalized_query = unidecode.unidecode(query).lower()
        cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)

        # Aplicar una coincidencia exacta con el `query` completo en cada campo, en el orden de las palabras
        filters = [
            DSMetaData.title.ilike(f"%{cleaned_query}%"),
            DSMetaData.description.ilike(f"%{cleaned_query}%"),
            Author.name.ilike(f"%{cleaned_query}%"),
            Author.affiliation.ilike(f"%{cleaned_query}%"),
            Author.orcid.ilike(f"%{cleaned_query}%"),
            FMMetaData.uvl_filename.ilike(f"%{cleaned_query}%"),
            FMMetaData.title.ilike(f"%{cleaned_query}%"),
            FMMetaData.description.ilike(f"%{cleaned_query}%"),
            FMMetaData.publication_doi.ilike(f"%{cleaned_query}%"),
            FMMetaData.tags.ilike(f"%{cleaned_query}%"),
            DSMetaData.tags.ilike(f"%{cleaned_query}%"),
        ]

        # Aplicar el filtro para la búsqueda exacta
        datasets = (
            self.model.query
            .join(DataSet.ds_meta_data)
            .join(DSMetaData.authors)
            .join(DataSet.feature_models)
            .join(FeatureModel.fm_meta_data)
            .filter(or_(*filters))
            .filter(DSMetaData.dataset_doi.isnot(None))  # Exclude datasets with empty dataset_doi
        )

        if publication_type != "any":
            matching_type = None
            for member in PublicationType:
                if member.value.lower() == publication_type:
                    matching_type = member
                    break

            if matching_type is not None:
                matching_type = next(
                    (member for member in PublicationType if member.value.lower() == publication_type), None
            )
            if matching_type:
                datasets = datasets.filter(DSMetaData.publication_type == matching_type.name)

        if tags:
            datasets = datasets.filter(DSMetaData.tags.ilike(any_(f"%{tag}%" for tag in tags)))

        # Order by created_at
        datasets = datasets.order_by(self.model.created_at.asc() if sorting == "oldest" else self.model.created_at.desc())

        return datasets.all()
