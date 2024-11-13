document.addEventListener('DOMContentLoaded', () => {
    send_query();
});

function send_query() {

    console.log("send query...")

    document.getElementById('results').innerHTML = '';
    document.getElementById("results_not_found").style.display = "none";
    console.log("hide not found icon");

    const filters = document.querySelectorAll('#filters input, #filters select, #filters [type="radio"]');

    filters.forEach(filter => {
        filter.addEventListener('input', () => {
            const csrfToken = document.getElementById('csrf_token').value;

            const searchCriteria = {
                csrf_token: csrfToken,
                query: document.querySelector('#query').value,
                publication_type: document.querySelector('#publication_type').value,
                sorting: document.querySelector('[name="sorting"]:checked').value,
                size: document.querySelector('#size').value, 
                author: document.querySelector('#authors').value, 
                files: document.querySelector('#files').value,
                title: document.querySelector('#title').value
            };

            console.log(document.querySelector('#publication_type').value);
            console.log(document.querySelector('#size').value);
            console.log(document.querySelector('#files').value);
            console.log(document.querySelector('#title').value);
            


            fetch('/explore', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(searchCriteria),
            })
            .then(response => response.json())
            .then(data => {

                console.log(data);
                document.getElementById('results').innerHTML = '';

                
                populateAuthorsFilter(data);
                populateTitleFilter(data);

                
                const filteredData = data.filter(dataset => {
                    const size = dataset.total_size_in_bytes;
                    const authorMatches = searchCriteria.author === "any" || dataset.authors.some(author => author.name === searchCriteria.author);
                    const titleMatches = 
                    searchCriteria.title === "any" || 
                    (Array.isArray(dataset.title) 
                        ? dataset.title.some(title => title === searchCriteria.title) 
                        : dataset.title === searchCriteria.title);
                    const files = dataset.files_count;

                    let sizeMatches = true;
                    switch (searchCriteria.size) {
                        case 'lessThan1KB':
                            sizeMatches = size < 1024;
                            break;
                        case 'between1KBand2KB':
                            sizeMatches = size >= 1024 && size < 2048;
                            break;
                        case 'between2KBand3KB':
                            sizeMatches = size >= 2048 && size < 3072;
                            break;
                        case 'between3KBand4KB':
                            sizeMatches = size >= 3072 && size < 4096;
                            break;
                        case 'between4KBand5KB':
                            sizeMatches = size >= 4096 && size < 5120;
                            break;
                        case 'moreThan5KB':
                            sizeMatches = size > 5120;
                            break;
                        default:
                            break;
                    }
                    
                    let filesMatches = true;
                    switch (searchCriteria.files) {
                        case "any":
                            filesMatches = true;
                            break;
                        case "1file":
                            filesMatches = files ==1;
                            break;
                        case "2files":
                            filesMatches = files ==2;
                            break;
                        case "3files":
                            filesMatches = files ==3;
                            break;
                        case "4files":
                            filesMatches = files ==4;
                            break;
                        case "5files":
                            filesMatches = files ==5;
                            break;
                        case "6files":
                            filesMatches = files ==6;
                            break;
                        case "7files":
                            filesMatches = files ==7;
                            break;
                        case "8files":
                            filesMatches = files ==8;
                            break;
                        case "9files":
                            filesMatches = files ==9;
                            break;
                        case "moreThan10files":
                            filesMatches = files > 10;
                            break;
                        default:
                            filesMatches = true;
                            break;
                    }
                    
                    return sizeMatches && authorMatches && filesMatches && titleMatches;
                });

                // results counter
                const resultCount = filteredData.length;
                const resultText = resultCount === 1 ? 'dataset' : 'datasets';
                document.getElementById('results_number').textContent = `${resultCount} ${resultText} found`;

                if (resultCount === 0) {
                    console.log("show not found icon");
                    document.getElementById("results_not_found").style.display = "block";
                } else {
                    document.getElementById("results_not_found").style.display = "none";
                }

                filteredData.forEach(dataset => {
                    let card = document.createElement('div');
                    card.className = 'col-12';
                    card.innerHTML = `
                        <div class="card">
                            <div class="card-body">
                                <div class="d-flex align-items-center justify-content-between">
                                    <h3><a href="${dataset.url}">${dataset.title}</a></h3>
                                    <div>
                                        <span class="badge bg-primary" style="cursor: pointer;" onclick="set_publication_type_as_query('${dataset.publication_type}')">${dataset.publication_type}</span>
                                    </div>
                                </div>
                                <p class="text-secondary">${formatDate(dataset.created_at)}</p>

                                <div class="row mb-2">
                                    <div class="col-md-4 col-12">
                                        <span class="text-secondary">Description</span>
                                    </div>
                                    <div class="col-md-8 col-12">
                                        <p class="card-text">${dataset.description}</p>
                                    </div>
                                </div>

                                <div class="row mb-2">
                                    <div class="col-md-4 col-12">
                                        <span class="text-secondary">Authors</span>
                                    </div>
                                    <div class="col-md-8 col-12">
                                        ${dataset.authors.map(author => `
                                            <p class="p-0 m-0">${author.name}${author.affiliation ? ` (${author.affiliation})` : ''}${author.orcid ? ` (${author.orcid})` : ''}</p>
                                        `).join('')}
                                    </div>
                                </div>

                                <div class="row mb-2">
                                    <div class="col-md-4 col-12">
                                        <span class="text-secondary">Tags</span>
                                    </div>
                                    <div class="col-md-8 col-12">
                                        ${dataset.tags.map(tag => `<span class="badge bg-primary me-1" style="cursor: pointer;" onclick="set_tag_as_query('${tag}')">${tag}</span>`).join('')}
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-md-4 col-12"></div>
                                    <div class="col-md-8 col-12">
                                        <a href="${dataset.url}" class="btn btn-outline-primary btn-sm" id="search" style="border-radius: 5px;">
                                            View dataset
                                        </a>
                                        <a href="/dataset/download/${dataset.id}" class="btn btn-outline-primary btn-sm" id="search" style="border-radius: 5px;">
                                            Download (${dataset.total_size_in_human_format})
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;

                    document.getElementById('results').appendChild(card);
                });
            });
        });
    });
}



function populateAuthorsFilter(data) {
    const authorsSet = new Set();
    data.forEach(dataset => {
        dataset.authors.forEach(author => {
            authorsSet.add(author.name);
        });
    });

    const authorsSelect = document.getElementById('authors');
    const currentAuthor = authorsSelect.value;
    authorsSelect.innerHTML = '<option value="any">Any</option>';

    authorsSet.forEach(author => {
        const option = document.createElement('option');
        option.value = author;
        option.textContent = author;
        authorsSelect.appendChild(option);
    });

    if (authorsSet.has(currentAuthor)) {
        authorsSelect.value = currentAuthor;
    }
}

function populateTitleFilter(data) {
    const titleSet = new Set();
    data.forEach(dataset => {
        titleSet.add(dataset.title);
    });

    const titleSelect = document.getElementById('title');
    const currentTitle = titleSelect.value;
    titleSelect.innerHTML = '<option value="any">Any</option>';

    titleSet.forEach(title => {
        const option = document.createElement('option');
        option.value = title;
        option.textContent = title;
        titleSelect.appendChild(option);
    });

    if (titleSet.has(currentTitle)) {
        titleSelect.value = currentTitle;
    }
}


function formatDate(dateString) {
    const options = {day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: 'numeric'};
    const date = new Date(dateString);
    return date.toLocaleString('en-US', options);
}

function set_tag_as_query(tagName) {
    const queryInput = document.getElementById('query');
    queryInput.value = tagName.trim();
    queryInput.dispatchEvent(new Event('input', {bubbles: true}));
}


function set_publication_type_as_query(publicationType) {
    const publicationTypeSelect = document.getElementById('publication_type');
    for (let i = 0; i < publicationTypeSelect.options.length; i++) {
        if (publicationTypeSelect.options[i].text === publicationType.trim()) {
            // Set the value of the select to the value of the matching option
            publicationTypeSelect.value = publicationTypeSelect.options[i].value;
            break;
        }
    }
    publicationTypeSelect.dispatchEvent(new Event('input', {bubbles: true}));
}


document.getElementById('clear-filters').addEventListener('click', clearFilters);

function clearFilters() {

    // Reset the search query
    let queryInput = document.querySelector('#query');
    queryInput.value = "";
    // queryInput.dispatchEvent(new Event('input', {bubbles: true}));

    // Reset the publication type to its default value
    let publicationTypeSelect = document.querySelector('#publication_type');
    publicationTypeSelect.value = "any"; // replace "any" with whatever your default value is
    // publicationTypeSelect.dispatchEvent(new Event('input', {bubbles: true}));

    // Reset the sorting option
    let sortingOptions = document.querySelectorAll('[name="sorting"]');
    sortingOptions.forEach(option => {
        option.checked = option.value == "newest"; // replace "default" with whatever your default value is
        // option.dispatchEvent(new Event('input', {bubbles: true}));
    });

    // Perform a new search with the reset filters
    queryInput.dispatchEvent(new Event('input', {bubbles: true}));
}

document.addEventListener('DOMContentLoaded', () => {

    //let queryInput = document.querySelector('#query');
    //queryInput.dispatchEvent(new Event('input', {bubbles: true}));

    let urlParams = new URLSearchParams(window.location.search);
    let queryParam = urlParams.get('query');

    if (queryParam && queryParam.trim() !== '') {

        const queryInput = document.getElementById('query');
        queryInput.value = queryParam
        queryInput.dispatchEvent(new Event('input', {bubbles: true}));
        console.log("throw event");

    } else {
        const queryInput = document.getElementById('query');
        queryInput.dispatchEvent(new Event('input', {bubbles: true}));
    }
});