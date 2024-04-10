// START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
// Please review links below and short commentary in readme.txt. Thank you.

// https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
// https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
// https://developer.mozilla.org/en-US/docs/Web/API/Headers
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify
// https://developer.mozilla.org/en-US/docs/Web/API/Response
// https://developer.mozilla.org/en-US/docs/Web/API/Window/location
async function createNewProtein(proteinData) {
    // send POST request to API 
    const response = await fetch('/api/protein/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            protein_id: proteinData.protein_id,
            sequence: proteinData.sequence,
            organism: proteinData.organism,
            length: proteinData.length,
            domains: proteinData.domains,
        }),
    });
    // if the response status is not ok, display an error
    if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
    }

    // after protein data submition redirect to the create_new_protein.html 
    window.location.href = '/bioscience_app/protein/create_new_protein/';
}

// END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
// Please review links below and short commentary in readme.txt. Thank you.