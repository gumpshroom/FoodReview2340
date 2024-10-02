var searchOpen = false
anime({
    targets: 'article',
    opacity: 1,
    duration: 1000,
    easing: 'cubicBezier(.5, .05, .1, .3)'
});
document.getElementById('searchInput').onfocus = function () {
    console.log("expand search")
    anime({
        targets: 'div#search',
        backgroundColor: '#FFF',
        duration: 500,
        width: '60%',
    });
    searchOpen = true
}
document.getElementById('searchInput').onblur = function () {
    console.log("shrink search")
    anime({
        targets: 'div#search',
        backgroundColor: '#FFF',
        duration: 500,
        width: '40%',
    });
    searchOpen = false
}
document.getElementById('searchInput').onkeydown = function (event) {
    if (event.key === 'Enter') {
        submitSearch()
    }
}

function doStars(stars) {
    console.log("do stars")
    var fullStars = Math.floor(stars);
    var halfStar = Math.round(stars - fullStars);
    var output = ""
    for (var i = 0; i < fullStars; i++) {
        output += '<i class="fill extra">star</i>';
    }
    if (halfStar) {
        output += ('<i class="fill extra">star_half</i>');
    }
    for (var i = 0; i < 5 - fullStars - halfStar; i++) {
        output += ('<i class="extra">star</i>');
    }
    return output
}

function doReviews(reviews) {
    console.log("do reviews")
    var output = "<div class='none small-height auto-width scroll'>"
    if (!reviews.length) {
        return "No reviews available"
    }
    reviews.forEach((review) => {
        output += `<article class='round'><div class="tiny-padding"><div class="grid"><div class="s1 m1 l1">`
        output += `<img class="tiny middle" src="${review.authorAttribution.photoURI}"></div>
                    <div class="s1 m1 l11"><p class="middle-align left-align small-margin large-text bold">${review.authorAttribution.displayName}</p></div>`
        output += `<div class="s2 m2 l12"><p class="responsive left-align top-align no-margin">${review.text}</p></div></div></div></article>`
    })
    return output + "</div>"
}

function addToFavorites(place_id, name, rating, address) {
    console.log('Adding to favorites:', place_id, name, rating);

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/users/addFavorites/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            'place_id': place_id,
            'name': name,
            'address': address,
            'rating': rating,
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`${name} has been added to your favorites!`);
            } else {
                alert(`${name} is already in your favorites.`);
            }
        })
        .catch(error => {
            alert('An error occurred while adding to favorites. Please try again.');
        });
}

async function submitSearch() {
    //get custom filters and stuff
    const {Place} = await google.maps.importLibrary("places");

    var query = document.getElementById('searchInput').value.trim()
    const request = {
        textQuery: query,
        fields: ["displayName", "primaryTypeDisplayName", "adrFormatAddress", "editorialSummary", "photos", "priceLevel", "rating", "userRatingCount", "reviews"],
        includedType: "restaurant",
        locationBias: {lat: 33.74969690485657, lng: -84.39235565742148},
        isOpenNow: true,
        language: "en-US",
        maxResultCount: 8,
        minRating: 3.2,
        region: "us",
        useStrictTypeFiltering: false,
    };

    const {places} = await Place.searchByText(request);
    if (places.length) {
        console.log(places)
        document.getElementById('results').innerHTML = ""

        places.forEach(async (place) => {
            console.log(place.displayName)

            const safeDisplayName = place.displayName.replace(/'/g, "\\'");

            var editorial = place.editorialSummary
            if (!place.editorialSummary) {
                editorial = await fetch("/generateDescription?restaurantName=" + place.displayName + "&restaurantType=" + place.primaryTypeDisplayName).then(response => response.text())
            }
            var AIopinion = await fetch("/summarizeComments?review1=" + (place.reviews.length ? place.reviews[0].text : "nothing") + "&reviewRandom=" + (place.reviews.length ? place.reviews[Math.floor(Math.random() * place.reviews.length)].text : "nothing")).then(response => response.text())

            var cardTemplate = `
<div class="padding" id="${place.id}">
        <article class="max large-padding center center-align pink1 large-round middle-align auto-width auto-height" style="opacity:0.3">
            <div style="width:100%" class="grid middle-align auto-height max">
                <div class="s1 m1 l6 auto-width">
                    <img class="medium-height center-align max" src="${place.photos[1].getURI()}" alt="" style="width:100%;height:100%;opacity:70%">
                    <div class="absolute top left right padding top-shadow white-text medium-height"><h5>${place.displayName}</h5>
                        <p>${place.primaryTypeDisplayName}</p></div>
                </div>
                <div class="s1 m2 l6">
                   
                        <div class="grid medium-height">
                        <div class="s1 m1 l12">
                        
                <nav class="tabbed small elevate">
                    <a class="active" data-ui="#overview-${place.id}" tabindex="0">
                        <i>info</i>
                        <span>Overview</span>
                    </a>
                    <a data-ui="#reviews-${place.id}" tabindex="0">
                        <i>group</i>
                        <span>Reviews</span>
                    </a>
                    <!--a data-ui="#map-${place.id}" tabindex="0">
                        <i>map</i>
                        <span>Map</span>
                    </a-->
                    
                </nav>
                
                
                        </div>
                        <div class="s1 m2 l12">
                        
                        <div class="page active" id="overview-${place.id}">
                        <div class="tiny-padding">
                        <div class="grid">
                            <div class="s1 m3 l12"> 
                                <div class="middle-align">
                                
                                ${doStars(place.rating)}
                                    
                                </div>
                                
                                
                            </div>
                            <div class="s1 m4 l6">
                            <h5 class="left-align">${place.rating} stars
                                <br><h6 class="small-text italic gray left-align">${place.userRatingCount} ratings</h6></h5>
                                <h6 class="small-text left-align gray">${(!place.priceLevel || place.priceLevel.charAt(0) === "F" || place.priceLevel.charAt(0) === "I") ? "$" : (place.priceLevel.charAt(0) === "M") ? "$$" : "$$$"} · ${place.priceLevel ? place.priceLevel.toLowerCase() : "no price data"}</h6>
                                <h6 class="small-text left-align gray">${place.adrFormatAddress.split(", ")[0] + ", Atlanta GA"}</h6>
</div>
<div class="s1 m4 l6 right-align">
                                <button class="round">View in Map</button>
                                <br><br>
                                <button class="border round" onclick="addToFavorites('${place.id}', '${safeDisplayName}', '${place.rating}', '${place.vicinity}')">Add to Favorites</button>
                            </div>
                            <hr>
                            <div class="s1 m12 l12">
                                <p class="left-align">${place.editorialSummary ? editorial : editorial + "<br><p class='italic small-text left-align'>Description generated by AI</p>"}</p>
                            </div>
                            
                            </div>
                            </div>
                            </div>
                            <div class="page" id="reviews-${place.id}">
                                <div class="tiny-padding none">
                                    
                                        ${doReviews(place.reviews)}
                                    
                                </div>
                                <div class ="s1 m2 l12">
                            <p class="italic small-text">AI says: ${AIopinion} </p>
</div>
                            </div>
                            </div>
                            
                            
                            
                        </div>
                    
                </div>
            </div>
        </article>
    </div>
`

            document.getElementById('results').innerHTML += cardTemplate
            anime({
                targets: 'article',
                opacity: 1,
                duration: 1000,
                easing: 'cubicBezier(.5, .05, .1, .3)'
            });

        });
    }
}