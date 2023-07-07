// Capture the DOM elements for the list, form and button using jQuery
const cupcakeList = $('ul.cupcake-list');
const formButton = $('button.add-cupcake');
const flavorForm = $('input.flavor-form');
const sizeForm = $('select.size-form');
const ratingForm = $('input.rating-form');
const imageForm = $('input.image-form');

// If you are running Flask on all routes, make sure to update the base URL
const baseURL = 'http://172.20.100.141:5000'

// Provide an anonymous function to execute upon clicking the submit button.
// The function should validate the form values (raise exceptions if they don't pass), create a JSON object to send
// to the API (POST request), and send a GET request to the API for all of the cupcakes to place on the list. 
formButton.on("click", async function(e){
    e.preventDefault();
    let flavorValue = flavorForm.val();
    let sizeValue = sizeForm.val();
    let ratingValue = ratingForm.val();
    let imageValue = imageForm.val();
    // Collect all the validate functions in an array and use a for...of loop to determine if any are false.
    // If just one is false, the form values will be reset and the function will cease.
    const total = [validateFlavor(flavorValue), validateRating(ratingValue), validateImage(imageValue)]
    for (let t of total){
        let result = validateIndividual(t);
        if (result != true){
            flavorForm.val('');
            sizeForm.val('');
            ratingForm.val('');
            imageForm.val('');
            return
        }
    }
     
    // Upon successful validation, create an object
    obj = {flavor: flavorValue, size: sizeValue, rating: ratingValue, image: imageValue};
    console.log(obj)
    // send a POST request to make an update to the cupcake database
    await axios.post(baseURL + '/api/cupcakes', obj);
    // delete all li elements from ul
    if (cupcakeList.children()){
        cupcakeList.empty();
    }
    // make a GET request to obtain an object of all cupcakes
    const cupcakes = await axios.get(baseURL + '/api/cupcakes');
    console.log(cupcakes)
    const allCupcakes = cupcakes['data']['cupcakes']
    console.log(allCupcakes)
    // run a for...of loop to append all cupcake flavors to list
    for (let cupcake of allCupcakes){
        cupcakeList.append(`<li>${cupcake['flavor']}</li>`);
    }
    // Empty the form values after operations have been completed
    flavorForm.val('');
    sizeForm.val('');
    ratingForm.val('');
    imageForm.val('');
    return
})

function validateFlavor(flav){
    if (flav == ''){
        return false
    }
    else {
        return true
    }
}

function validateRating(rate){
    if (isNaN(rate) || rate < 0 || rate > 10){
        return false
    }
    else {
        return true
    }
}

function validateImage(imag){
    if (typeof imag != 'string' || imag instanceof String || imag != ''){
        return false
    }
    else {
        return true
    }
}

function validateIndividual(valid){
    if (valid == true){
        return true
    }
    else{
        return false
    }
}