
function fade_replace( block1, block2 )
{
	block1.animate({
		opacity: 0,
	}, 
	"slow",
		function(){

			block2.css('opacity', 0);
			block2.css('display', 'block' );

			block1.css('display', 'none');


			block2.animate({
				opacity: 1
			}, 
			"fast",
				function(){
				}
			);

		}
	);
}

function fade_out( block )
{
	block.animate({
		opacity: 0,
	}, 
	"slow",
		function(){
			block.css('display', 'none');
		}
	);
}

function fade_in( block )
{
	block.css('display', 'block');
	block.animate({ opacity: 1, }, "slow");
}




