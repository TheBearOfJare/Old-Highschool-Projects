//helper functions
function randrange(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function encrypt(method) {

	message = document.getElementById('message').value

	while(message.includes(' ')) {
		message = message.replace(' ','')
	}
	message = message.toLowerCase()
	
	data = eval(`${method}('${message}')`)

	encrypted_message = data[0]
	notes = data[1]
	
	output = document.getElementById('output')
	output.value = encrypted_message + '\n\n' + notes

	output.style.display = 'block'
	output.focus()
}

function Ceaser_cypher(message) {

	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	
	shifted_alphabet = []
	shift = randrange(1,25)
	console.log('shift: '+shift)
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
	
	return [shifted_message, `the message was shifted ${shift} letters forward in the alphabet`]
	
	
}

function Picket_fence(message) {

	message_odds = []
	message_evens = []

	for (index = 0; index < message.length; index++) {
		if (index%2 === 0) {
			message_odds.push(message[index])
		}
		else {
			message_evens.push(message[index])
		}
	}

	order = randrange(0,1)
	if (order === 0) {
		newmessage = message_evens.join('') + message_odds.join('')
		notes = 'evens were placed before odds'
	}

	else {
		newmessage = message_odds.join('') + message_evens.join('')
		notes = 'odds were placed before evens'
	}
	
	return [newmessage, notes]
		
}

function Random_substitution(message) {
	
}

function Greek_square(message) {
	
}