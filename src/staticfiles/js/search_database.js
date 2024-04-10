// START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
// Please review links below and short commentary in readme.txt. Thank you.

// https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement
// https://developer.mozilla.org/en-US/docs/Web/API/Node/appendChild
// https://developer.mozilla.org/en-US/docs/Web/API/HTMLLabelElement
// https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement
// https://developer.mozilla.org/en-US/docs/Glossary/Recursion
function createSearchResultForm(data) {
    const form = document.createElement("form"); // create a new form element
    form.className = "form-result"; // add new class name
    // loop through each key-value pair in the data 
    for (const key in data) {
        const value = data[key];
        const label = document.createElement("label"); // create a new label element for key

        label.textContent = key + ":"; // set the label's text content to key

        // check if value is an object & and not null
        if (typeof value === "object" && value !== null) {
            const subForm = createSearchResultForm(value); // if all conditions were met, create a sub-form
            label.appendChild(subForm); // add sub-form to the label
        } else {
            const input = document.createElement("input"); // otherwise, create a new input element 
            input.setAttribute("name", key); // set input's name to the key
            input.setAttribute("value", value); // set input's value to value
            label.appendChild(input); // add input to the label
        }

        form.appendChild(label); // add  label + child to the form
    }

    return form; // return the form
}

// https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById
// https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/Trim
// https://developer.mozilla.org/en-US/docs/Web/API/Window/alert

function SearchSectionSetup(inputId, buttonId, apiUrl, resultContainerId) {
    const input = document.getElementById(inputId);
    const button = document.getElementById(buttonId);

    // check if input and button elements exist
    if (input === null || button === null) {
        return; // if dont exist, dont set up search section 
    }

    // add onclick event handler for the button 
    button.onclick = async function(event) {
        event.preventDefault();

        try {
            // check if input is valid
            if (input.value.trim().length === 0) {
                throw new Error("Please enter a valid search term");
            }
            console.log("Search value:", input.value);

            // use showData to get and display data
            await showData(apiUrl + input.value, resultContainerId);
            // display search section after the search is finished
            document.getElementById("search-section").style.display = "block";
        } catch (validationError) {
            // display validation error message
            alert(validationError.message);
        }
        // blocks from refreshing of the page
        return false;
    };
}

// https://developer.mozilla.org/en-US/docs/Web/API/Document/addEventListener
// https://developer.mozilla.org/en-US/docs/Web/API/Window/DOMContentLoaded_event
// https://developer.mozilla.org/en-US/docs/Glossary/Callback_function
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/function
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_Operator
function SearchSections(callback) {
    // search section for proteins set up
    SearchSectionSetup('protein_input', 'protein_button', '/api/protein/', 'protein_result');
    // search section for Pfam domains set up
    SearchSectionSetup('pfam_input', 'pfam_button', '/api/pfam/', 'pfam_result');
    // search section for proteins by taxa
    SearchSectionSetup('proteinsOfTaxa_input', 'proteinsOfTaxa_button', '/api/proteins/', 'proteinsOfTaxa_result');
    // search section for Pfam domains by taxa
    SearchSectionSetup('pfamsOfTaxa_input', 'pfamsOfTaxa_button', '/api/pfams/', 'pfamsOfTaxa_result');
    // search section for for coverage
    SearchSectionSetup('coverage_input', 'coverage_button', '/api/coverage/', 'coverage_result');

    // if callback provided
    if (callback) {
        callback();
    }
}

// call Search Sections when the DOM loaded
document.addEventListener('DOMContentLoaded', function() {
    SearchSections();
});

// https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector
// https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault
// https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style
// https://developer.mozilla.org/en-US/docs/Web/API/EventListener
// https://developer.mozilla.org/en-US/docs/Web/API/Element/classList

// check if search button exists 
var searchDatabaseButton = document.querySelector(".dashboard-search .btn-info");
if (searchDatabaseButton) {
    // get search section container
    var searchSection = document.querySelector("#search-section");

    // add event listener
    searchDatabaseButton.addEventListener("click", function(event) {
        // block default behavior of <a> 
        event.preventDefault();

        // display search section
        searchSection.style.display = "block";
    });

    // add event listener to search button
    document.querySelector(".search-db").addEventListener("click", function(e) {
        e.preventDefault();
        document.querySelector("#search-section").classList.remove("d-none");
    });
}

// END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
// Please review links below and short commentary in readme.txt. Thank you.