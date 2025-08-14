// Array of events
const events = [
    { name: 'Music Concert', date: 'Dec 14, 2024', time: '7:00 PM', location: 'Indiranagar', description: 'Get ready for a night of face-melting solos and headbanging anthems! 🤟 Join us for Jass Time, featuring Anirudh, as they bring their unique brand of  music 🎵 to the stage! Do not miss out on the heavy riffs and epic vocals' },
    { name: ' Food Culture', date: 'Dec 17, 2024', time: '6:00 PM', location: 'Indiranagar', description: 'Food is more than just sustenance - it is a way to connect with our heritage, our community, and our senses 🍴. In Bengaluru, we are proud to celebrate our diverse food culture, from traditional family recipes to innovative fusion cuisine 🍜.' },
    { name: 'Music Nights', date: 'Nov 30, 2024', time: '11:00 PM', location: 'Lingarajapuram', description: 'Get ready for an unforgettable night of music! Join us for Music Nights 🎵 , featuring AR Rahaman. Enjoy a live performance of their hit songs and experience the energy of a live concert.'}, 
    { name: 'Art Exhibition', date: 'Oct 18, 2024', time: '2:00 PM', location: 'Ulsoor', description: 'Immerse yourself in the world of art and creativity 🎨! Our upcoming exhibition features an incredible collection of works by local and international artists 🌎. From paintings and sculptures to installations and photography, every piece tells a unique story and invites you to explore new perspectives 🔍.' },
    { name: 'Food Festival', date: 'Nov 5, 2024', time: '12:00 PM', location: 'JPnagar', description: 'In Bengaluru, food is a way of life 🍴. Our local events celebrate the rich culinary heritage of our community, from traditional cooking techniques to modern twists and innovations 🔥.' },
    { name: 'Tech Conference', date: 'Oct 20, 2024', time: '10:00 AM', location: 'Jayanagar', description: 'Join the conversation that is shaping the future of tech 💬! Our conference features keynote speakers, panel discussions, and workshops on the latest technologies and innovations 📊. Network with fellow tech enthusiasts, learn from industry experts, and discover new opportunities for growth and collaboration 🤝. ' },
    { name: 'Yoga Retreat', date: 'Nov 10, 2024', time: '6:00 AM', location: 'Marathahalli', description: '"Escape to a serene oasis and rejuvenate your body, mind, and spirit 🌴! Our yoga retreat offers a tranquil getaway from the stresses of everyday life, where you can immerse yourself in the practice of yoga and connect with like-minded individuals 🧘‍♀.' },
    { name: 'Literature Fest', date: 'Oct 23, 2024', time: '1:00 PM', location: 'Banashankari', description: 'Get ready to indulge in a world of words and ideas 📚! Our literature festival brings together renowned authors, poets, and thinkers for a celebration of literature in all its forms 🎉.' },
    { name: 'Film Screening', date: 'Nov 2, 2024', time: '8:00 PM', location: 'Hebbal', description: 'Step into the world of cinema and experience the magic of the movies 🎥! Our film screening showcases a diverse range of films, from classics to contemporary releases, and from documentaries to feature films 📽.' },
    { name: 'Charity Run', date: 'Nov 12, 2024', time: '7:00 AM', location: 'Yelahanka', description: 'Lace up your running shoes and join us for a charity run that will make a difference in your community 🏃‍♀! Our event supports Annai Theresa, which works tirelessly to charity Run. Every step you take will help bring us closer to our goal of [fundraising goal] 🏆.' },
    { name: 'Yogasana', date: 'Dec 14, 2024', time: '7:00 PM', location: 'MGroad', description: 'Find your inner peace and connect with nature 🌿! Our yoga retreat takes place in a stunning natural setting, where you can practice yoga, meditation, and other holistic activities amidst breathtaking scenery ' },
    { name: 'The Royal Gallop', date: 'Dec 17, 2024', time: '6:00 PM', location: 'Electronic City', description: '🔥🐴 Get ready for the ultimate adrenaline rush! The Horse rides is a heart-pumping, action-packed horse racing event that will keep you on the edge of your seat. 🎢 Watch as the fastest horses in the world thunder down the track, their manes flowing in the wind.' },
    { name: 'Tech Talk Shows', date: 'Nov 30, 2024', time: '11:00 PM', location: 'Lingarajapuram', description: 'Get ready to revolutionize your world with the latest tech trends and innovations 🚀! Our tech conference brings together the brightest minds in the industry to share their insights and expertise 💡.' },
    { name: 'Hip-Hop Concerts', date: 'Dec 20, 2024', time: '6:00 PM', location: 'Kammanahalli', description: 'Get ready to turn up the volume and vibe out with the hottest names in hip hop 🎤! Our concert features an unforgettable lineup of artists, from old-school legends to new-school trailblazers .' },
];

// Render events as trending topics
function displayEvents(eventsToDisplay) {
    const eventContainer = document.getElementById('event-container');
    eventContainer.innerHTML = '';
    eventsToDisplay.forEach(event => {
        const eventCard = document.createElement('div');
        eventCard.classList.add('event-card');
        eventCard.innerText = event.name;
        eventCard.onclick = () => openModal(event);
        eventContainer.appendChild(eventCard);
    });
}
// Filter events based on search
function filterEvents() {
    const search = document.getElementById('search').value.toLowerCase();
    const location = document.getElementById('location').value.toLowerCase();
    const filteredEvents = events.filter(event =>
        event.name.toLowerCase().includes(search) &&
        event.location.toLowerCase().includes(location)
    );
    displayEvents(filteredEvents);
}

// Open modal with event details
function openModal(event) {
    document.getElementById('modalEventName').innerText = event.name;
    document.getElementById('modalEventDate').innerText = event.date;
    document.getElementById('modalEventTime').innerText = event.time;
    document.getElementById('modalEventLocation').innerText = event.location;
    document.getElementById('modalEventDescription').innerText = event.description;
    document.getElementById('eventModal').style.display = 'flex';
}

// Close the modal
function closeModal() {
    document.getElementById('eventModal').style.display = 'none';
}
// Initial display of trending topics
displayEvents(events);

