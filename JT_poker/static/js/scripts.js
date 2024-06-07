document.addEventListener('DOMContentLoaded', function() {
    const wsUrl = 'ws://' + window.location.host + '/ws/playPoker/';
    const chatSocket = new WebSocket(wsUrl);
    const staticUrl = document.querySelector('script[src*="scripts.js"]').src.replace('js/scripts.js', 'images/cards/Deck1/');
    let displayedMessages = [];
    let displayedCardImages = [];

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'update_player_info') {
            const playerInfoContainer = document.getElementById('playerInfo');
            if (playerInfoContainer) {
                playerInfoContainer.textContent = JSON.stringify(data.player_info, null, 2);
            }
        } else if (data.type === 'update_messages') {
            const messagesContainer = document.getElementById('messagedisplay');
            messagesContainer.innerHTML = ''; // Clear previous messages
            const messages = data.messages.slice(-20); // Only take the last 20 messages
            messages.forEach(message => {
                const messageDiv = document.createElement('div');
                messageDiv.textContent = message;
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            });
            displayedMessages = messages;
        } else if (data.type === 'update_card_images') {
            const cardsContainer = document.getElementById('cards');
            cardsContainer.innerHTML = ''; // Clear previous card images
            data.card_images.forEach((card, index) => {
                const cardDiv = document.createElement('div');
                cardDiv.className = 'card-player';
                cardDiv.dataset.selected = '0';
                cardDiv.dataset.order = index;
                cardDiv.dataset.originalOrder = index;
                console.log('Card:', card, 'Original Order:', cardDiv.dataset.originalOrder, 'selected:', cardDiv.dataset.selected);

                const button = document.createElement('button');
                const img = document.createElement('img');
                img.src = staticUrl + card.trim();
                img.draggable = true;
                button.appendChild(img);
                cardDiv.appendChild(button);

                button.addEventListener('click', function() {
                    cardDiv.classList.toggle('selected');
                    cardDiv.dataset.selected = cardDiv.classList.contains('selected') ? '1' : '0';
                    console.log(generateDiscardString()); // Debug: Log the discard string
                });

                img.addEventListener('dragstart', function(event) {
                    event.dataTransfer.setData('text/plain', cardDiv.dataset.order);
                });

                img.addEventListener('touchstart', function(event) {
                    touchStartX = event.touches[0].clientX;
                    touchStartY = event.touches[0].clientY;
                    draggedElement = cardDiv;
                    event.dataTransfer = {}; // Simulate dataTransfer for touch
                    event.dataTransfer.setData = function(type, val) {
                        this[type] = val;
                    };
                    event.dataTransfer.getData = function(type) {
                        return this[type];
                    };
                    event.dataTransfer.setData('text/plain', cardDiv.dataset.order);
                });

                cardsContainer.addEventListener('dragover', function(event) {
                    event.preventDefault();
                });

                cardsContainer.addEventListener('touchmove', function(event) {
                    event.preventDefault();
                    const touch = event.touches[0];
                    const targetElement = document.elementFromPoint(touch.clientX, touch.clientY);
                    const targetCard = targetElement.closest('.card-player');
                    if (targetCard && draggedElement) {
                        const sourceOrder = draggedElement.dataset.order;
                        const targetOrder = targetCard.dataset.order;
                        const sourceCard = document.querySelector(`.card-player[data-order="${sourceOrder}"]`);
                        const targetCardElement = document.querySelector(`.card-player[data-order="${targetOrder}"]`);

                        if (sourceCard !== targetCardElement) {
                            const sourceParent = sourceCard.parentNode;
                            const targetParent = targetCardElement.parentNode;

                            const sourceNext = sourceCard.nextSibling === targetCardElement ? sourceCard : sourceCard.nextSibling;
                            targetParent.insertBefore(sourceCard, targetCardElement);
                            sourceParent.insertBefore(targetCardElement, sourceNext);
                        }
                    }
                });

                cardDiv.addEventListener('drop', function(event) {
                    event.preventDefault();
                    const sourceOrder = event.dataTransfer.getData('text/plain');
                    const targetOrder = this.dataset.order;
                    const sourceCard = document.querySelector(`.card-player[data-order="${sourceOrder}"]`);
                    const targetCard = document.querySelector(`.card-player[data-order="${targetOrder}"]`);

                    if (sourceCard !== targetCard) {
                        const sourceParent = sourceCard.parentNode;
                        const targetParent = targetCard.parentNode;

                        const sourceNext = sourceCard.nextSibling === targetCard ? sourceCard : sourceCard.nextSibling;
                        targetParent.insertBefore(sourceCard, targetCard);
                        sourceParent.insertBefore(targetCard, sourceNext);
                    }
                });

                cardDiv.addEventListener('touchend', function(event) {
                    if (draggedElement) {
                        const touch = event.changedTouches[0];
                        const targetElement = document.elementFromPoint(touch.clientX, touch.clientY);
                        const targetCard = targetElement.closest('.card-player');
                        if (targetCard) {
                            const sourceOrder = draggedElement.dataset.order;
                            const targetOrder = targetCard.dataset.order;
                            const sourceCard = document.querySelector(`.card-player[data-order="${sourceOrder}"]`);
                            const targetCardElement = document.querySelector(`.card-player[data-order="${targetOrder}"]`);

                            if (sourceCard !== targetCardElement) {
                                const sourceParent = sourceCard.parentNode;
                                const targetParent = targetCardElement.parentNode;

                                const sourceNext = sourceCard.nextSibling === targetCardElement ? sourceCard : sourceCard.nextSibling;
                                targetParent.insertBefore(sourceCard, targetCardElement);
                                sourceParent.insertBefore(targetCardElement, sourceNext);
                            }
                        }
                        draggedElement = null;
                    }
                });

                cardsContainer.appendChild(cardDiv);
            });
            displayedCardImages = data.card_images;
        } else if (data.type === 'game_started') {
            alert(data.message);
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    function generateDiscardString() {
        let discardString = '';
        const cards = document.querySelectorAll('.card-player');
        cards.forEach(card => {
            discardString += card.dataset.selected;
        });
        return discardString;
    }

    document.getElementById('play-button').addEventListener('click', function() {
        chatSocket.send(JSON.stringify({
            'type': 'start_game'
        }));
    });

    document.getElementById('play-button').addEventListener('touchstart', function() {
        chatSocket.send(JSON.stringify({
            'type': 'start_game'
        }));
    });

    function disableButtons() {
        const playButton = document.querySelector('button[name="play"]');
        playButton.disabled = true;
    }
});