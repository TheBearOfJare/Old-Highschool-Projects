var words = []

//fetch the dictionary
var client = new XMLHttpRequest();
client.open('GET', '/words.txt');
client.onreadystatechange = function() {
  words = client.responseText
}
client.send();


function decrypt() {
	message = document.getElementById('message').value
	output = []
	options = ceaser(message)

	//find the best most plausible solutions
	
	best = {'none': 0}
	
	for (option = 0; option < options.length; option++) {
			
		score = 0
		
		for (word = 0; word < words.length; word++) {
			
			if (options[option].includes(words[word])) {
				score++
			}
		}
		if (score > 0) {
			
			best[options[option]] = score
		}
	
	}


	var items = Object.keys(best).map(function(key) {
	  return [key, best[key]];
	});
	
	items.sort(function(first, second) {
	  return second[1] - first[1];
	});

	best = items
	for (entry = 0; entry < best.length; entry++) {
		if (entry >= 5 ) {
			break
		}
		console.log(best[entry])
		output.push(best[entry][0])
	}

	output = output.join('\n\n')

	box = document.getElementById('output')
	box.value = 'Possible decryptions are:\n\n'+output
	box.style.display = 'block'
}


function ceaser(message) {

	message.toLowerCase()
	alphabet = 'abcdefghijklmnopqrstuvwxyz'

	shifted_messages = []
	for (shift = 1; shift < alphabet.length; shift++) {
		
		shifted_alphabet = []
		//console.log('shift: '+i)
		index = shift
	
		shifted_message = []
		//console.log(alphabet.length)
		for (i = 0; i < alphabet.length; i++) {
			if (index >= alphabet.length) {
				index-=26
			}
			//console.log(alphabet[index])
			shifted_alphabet.push(alphabet[index])
			index++
		}
		
		console.log(shifted_alphabet)
	
		for (i = 0; i < message.length; i++) {
			shifted_message.push(shifted_alphabet[alphabet.indexOf(message[i])])
		}
		
		shifted_message = shifted_message.join('')

		shifted_messages.push(shifted_message)
		
	}	

	console.log(shifted_messages)
	return shifted_messages
	
}

function picket(message) {
	
}