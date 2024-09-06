let cy;
let animationInterval;
let currentRound = 0;
let currentStep = 0;
let simulationData;
let isPaused = false;

function loadSimulationData() {
return fetch('/simulation-result')
    .then(response => response.json())
    .then(data => {
        simulationData = data.simulation;
    });
}

// Function to get node data by ID from the simulation data
function getNodeDataById(nodeId) {
user_data = simulationData[currentRound].result[currentStep].user_data
for (let user of user_data) {
    if (user.id.toString() === nodeId) {
        return user;
    }
}
return null;
}


function colorMapping(status) {
switch (status) {
    case 0: return '#ff0000'; // Red
    case 1: return '#00ff00'; // Green
    default: return '#cccccc'; // Grey
}
}

function updateNodeColors(stepData) {
stepData.user_data.forEach(user => {
    cy.getElementById(user.id.toString()).style('background-color', colorMapping(user.status));
});
}

function parseResponse(text) {
const jsonRegex = /{[^}]*"response"[^}]*"opinion"[^}]*"phrases"[^}]*}/;
const match = text.match(jsonRegex);

if (match) {
    const jsonString = match[0];

    try {
        const jsonData = JSON.parse(jsonString);
        return jsonData;
    } catch (e) {
        console.error("Failed to parse JSON:", e);
        return null;
    }
} else {
    console.error("JSON not found in the text.");
    return null;
}
}

function updateTooltip(nodeId) {
const nodeData = getNodeDataById(nodeId);
if (nodeData && nodeData.posts && nodeData.posts.length > 0) {
    const lastPost = nodeData.posts[nodeData.posts.length - 1];
    const lastPostData = parseResponse(lastPost);
    return `
        <strong>Last Post:</strong><br>
        ${lastPostData.response}<br>
        Opinion: ${lastPostData.opinion}<br>
        Phrases: ${lastPostData.phrases}
    `;
} else {
    return "No posts available";
}
}

function startAnimation() {
if (!isPaused) {
    currentRound = 0;
    currentStep = 0;
}

isPaused = false;

animationInterval = setInterval(() => {
    if (currentRound < simulationData.length) {
        const roundData = simulationData[currentRound].result;

        if (currentStep < roundData.length) {
            currentSimulationData = roundData[currentStep]
            updateNodeColors(roundData[currentStep]);
            currentStep++;
        } else {
            // Move to the next round
            currentRound++;
            currentStep = 0;

            if (currentRound < simulationData.length) {
                // Initialize the first step of the next round
                updateNodeColors(simulationData[currentRound].result[currentStep]);
            } else {
                clearInterval(animationInterval); // End of all rounds
            }
        }
    } else {
        clearInterval(animationInterval); // End of all rounds
    }
}, 3000);
}


function pauseAnimation() {
clearInterval(animationInterval);
isPaused = true;
}

function resetAnimation() {
clearInterval(animationInterval);
currentRound = 0;
currentStep = 0;
isPaused = true;
cy.nodes().style('background-color', '#cccccc'); // Reset all node colors to grey
}

document.getElementById('start-btn').addEventListener('click', startAnimation);
document.getElementById('pause-btn').addEventListener('click', pauseAnimation);
document.getElementById('reset-btn').addEventListener('click', resetAnimation);

function loadGraph() {
fetch('/simulation-graph')
    .then(response => response.json())
    .then(data => {
        const elements = [];

        // Populate elements with nodes
        data.graph_data.nodes.forEach(node => {
            elements.push({
                data: {
                    id: node.id.toString(),
                    label: node.label ? node.label : `${node.id}`,
                    profile: node.profile
                }
            });
        });

        // Populate elements with edges
        data.graph_data.edges.forEach(edge => {
            elements.push({
                data: {
                    source: edge[0].toString(),
                    target: edge[1].toString()
                }
            });
        });

        // Initialize Cytoscape with the elements
        if (cy) {
            cy.destroy(); // Destroy the previous instance if it exists
        }

        cy = cytoscape({
            container: document.getElementById('cy'),
            elements: elements,
            style: [
                {
                    selector: 'node',
                    style: {
                        'label': 'data(label)',
                        'width': 20,
                        'height': 20,
                        'background-color': '#cccccc',
                        'text-valign': 'center',
                        'text-halign': 'center',
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 1,
                        'line-color': '#999'
                    }
                }
            ],
            layout: {
                name: 'grid', // 'cose' or 'grid', 'circle', etc.
                fit: true,
                padding: 10
            }
        });

        // Tooltip setup
        const tooltip = document.createElement('div');
        tooltip.className = 'cy-tooltip';
        document.getElementById('cy').appendChild(tooltip);

        cy.on('click', 'node', function(evt) {
            const node = evt.target;
            const nodeData = elements.find(el => el.data.id === node.id());

            if (nodeData && nodeData.data.profile) {
                const content = `
                    <strong>${nodeData.data.profile.Name}</strong><br>
                    Location: ${nodeData.data.profile.Location}<br>
                    Age: ${nodeData.data.profile.Age}<br>
                    Gender: ${nodeData.data.profile.Gender}<br>
                    Occupation: ${nodeData.data.profile.Occupation}<br>
                    ${nodeData.data.profile.Description}
                `;
                tooltip.innerHTML = content;
                tooltip.style.display = 'block';

                const position = node.renderedPosition();
                tooltip.style.left = (position.x + 15) + 'px';
                tooltip.style.top = (position.y - tooltip.offsetHeight - 15) + 'px';
            }
        });

        cy.on('mouseover', 'node', function(evt) {
            const node = evt.target;
            const tooltipContent = updateTooltip(node.id());

            tooltip.innerHTML = tooltipContent;
            tooltip.style.display = 'block';

            const position = node.renderedPosition();
            tooltip.style.left = (position.x + 15) + 'px';
            tooltip.style.top = (position.y - tooltip.offsetHeight - 15) + 'px';
        });

        cy.on('mouseout', 'node', function() {
            tooltip.style.display = 'none';
        });
    })
    .catch(error => console.error('Error loading graph:', error));
}

document.addEventListener('DOMContentLoaded', () => {
loadSimulationData();
loadGraph(); // Ensure the graph is loaded when the page is ready
});