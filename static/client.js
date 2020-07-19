$(function(){
		var vacs= new Array();
    var removed= new Array();
		$('.button').on('click', function(){
			var id= $(this).attr('id');
      if(vacs.includes(id.toString())){
        vacs.splice(vacs.indexOf(id), 1);
        console.log('removed');
        $(this).css('background-color','#d3d3d3');
        removed.push(id);
      }
      else{
          console.log('added');
          $(this).css('background-color','red');
          vacs.push(id);
          console.log(vacs);
      }
    })
    
		$('.cutout').on('click', function(){
			console.log(vacs);
      $.ajax({
        url: '/hmiside',
        type: 'GET',
        data: {"vacs" : JSON.stringify(vacs)}, 
        })
        .done(function(result){     // on success get the return object from server
            console.log("info_val "+ result)
            $('#info_val').html('<b>Information Value (UINT32) at HMI: </b>'+ result);
            $.ajax({
            url: '/bb08side',
            type: 'GET',
            data: {"info_val" : JSON.stringify(result)}, 
            })
            .done(function(result){     // on success get the return object from server
                console.log("BB08 side "+ result)
                $('#bin_rep').html('<b>Binary Representation (R->L) at Core level: </b>'+ result);
                $('#note').css('display','block');
            })
        })
      for (var i = removed.length - 1; i >= 0; i--) {
				document.getElementsByName(removed[i])
		  .forEach((el) => {
		    el.setAttribute("fill", "white");
		  });
			}
			for (var i = vacs.length - 1; i >= 0; i--) {
				document.getElementsByName(vacs[i])
		  .forEach((el) => {
		    el.setAttribute("fill", "#f0ada3");
		  });
			}
		})
	})