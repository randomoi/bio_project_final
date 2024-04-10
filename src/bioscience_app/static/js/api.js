// START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
// Please review links below and short commentary in readme.txt. Thank you.

// https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
// https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse
async function fetchDataURL(url) {
    const response = await fetch(url); // send API request 

    if (!response.ok) { // if response is not ok, throw an error
        throw new Error(`API request failed with status ${response.status}`);
    }

    const data = await response.json(); // parse response data and await for it to be returned

    // check for custom error message 
    if (data.error) {
        throw new Error(data.error); // if yes, throw an error with custom message
    }

    return data; // return parsed data
}

// https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById
// https://developer.mozilla.org/en-US/docs/Web/API/Node/removeChild
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/isArray
// https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement
// https://developer.mozilla.org/en-US/docs/Web/API/Element/setAttribute
// https://developer.mozilla.org/en-US/docs/Web/API/Node/appendChild
async function showData(url, resultContainerId) {
    const resultContainer = document.getElementById(resultContainerId);

    // clear content before fetching new data
    while (resultContainer.firstChild) {
        resultContainer.removeChild(resultContainer.firstChild);
    }

    try {
        const data = await fetchDataURL(url); // fetch data 

        const toggleButton = document.createElement("button");
        toggleButton.textContent = "Hide";
        toggleButton.classList.add("btn", "btn-link", "collapsed");
        toggleButton.setAttribute("data-toggle", "collapse");
        toggleButton.setAttribute("data-target", `#${resultContainerId}-collapsible`);
        resultContainer.appendChild(toggleButton); // add a toggle button 
        // collapsible feature
        const collapsibleDiv = document.createElement("div");
        collapsibleDiv.classList.add("collapse", "show"); // add show class to display collapsible content 
        collapsibleDiv.setAttribute("id", `${resultContainerId}-collapsible`);

        if (typeof data === 'object' && data !== null) { // check if data is an object and not null
            if (Array.isArray(data)) { // if data is an array
                data.forEach(item => {
                    collapsibleDiv.appendChild(createSearchResultForm(item)); // create a form for each item in the array and add it to the result 
                });
            } else {
                collapsibleDiv.appendChild(createSearchResultForm(data));
            }
        } else {
            collapsibleDiv.textContent = "Nothing to display ;("; // display message 
        }

        resultContainer.appendChild(collapsibleDiv);

        // add event listener to show or hide toggle button 
        toggleButton.addEventListener("click", function() {
            collapsibleDiv.classList.toggle("collapse");
            if (toggleButton.textContent === "Unhide") {
                toggleButton.textContent = "Hide";
            } else {
                toggleButton.textContent = "Unhide";
            }
        });

    } catch (error) {
        console.error("showData Error:", error.message);
        // custom error message setup 
        const errorMessage = document.createElement("div"); // create new div for error message
        errorMessage.className = "error-message"; // add a class for css
        errorMessage.textContent = error.message; // add textContent to error message
        resultContainer.appendChild(errorMessage); // add error message to result 
    }
    console.log("showData finished.");
}

// END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
// Please review links below and short commentary in readme.txt. Thank you.