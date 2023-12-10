$(document).ready(function() {
  $('.product-box').each(function() {
    var starRating = $(this).find('.star-rating');

    starRating.on('mouseenter', function() {
      var ratingValue = $(this).data('rating');
      // Fills all the stars until the current one
      starRating.slice(0, ratingValue).css('color', 'black');
    });

    starRating.on('mouseleave', function() {
      // Resets all the stars to the original color
      starRating.css('color', '#ccc');
    });

    starRating.on('click', function() {
      var productId = $(this).data('product_id');
      var ratingValue = $(this).data('rating');

      console.log(productId)
      console.log(ratingValue)

      $.ajax({
        type: 'PUT',
        url: `/etienda/api/products/${productId}/${ratingValue}`,
        headers: {
          'Authorization': 'Bearer dai',
        },
        success: function(data) {
          // Updates the user interface after the rating has been updated successfully
          var averageRatingElement = $('#average-rating-' + productId);
          var ratingCountElement = $('#rating-count-' + productId);
          averageRatingElement.text('Rating: ' + data.rating.rate);
          ratingCountElement.text('Number of ratings: ' + data.rating.count);
          console.log('Rating updated successfully:', data);
        },
        error: function(error) {
          console.error('Error updating rating:', error);
        }
      });
    });
  });
});
