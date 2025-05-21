"""
(c) 2024, CatSalut. Servei Català de la Salut
License: Apache 2.0
Author: Martin A. Koch, PhD
"""

import pandas as pd

import customtkinter
from customtkinter import filedialog
import webbrowser

def my_gui():
	def make_visualization(output_folder):

		#html texts
		content1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content {{CKMURL}}</title>
    <!-- BoxIcons -->
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
		html{
			min-height:100vh;
			height: 100vh;
			padding: 0px;
			margin: 0px;
           
		}
	
        body {
			font: 10pt arial;
			min-height:100vh;
			height: 100vh;
            overflow: hidden;
        }

        #mainContent {
            display: flex;
			height:100%;
            flex-grow: 1;
            position: relative;
        }

        #network {
            flex-grow: 1;
            height: 100%;
            width: 100%;
            position: relative;
			z-index: 1;
            background-color: white;
        }

        #headerOverlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 500px;
            padding: 10px;
            background: rgba(255, 255, 255, 0.5);
            text-align: left;
            z-index: 2;
            pointer-events: none;
            border-radius: 20pt;
        }
		
		 #infoOverlay {
            position: absolute;
            top: 90%;
            left: 0;
            width: 300px;
            padding: 10px;
            background: rgba(255, 255, 255, 0.5);
            text-align: left;
            z-index: 2;
            border-radius: 20pt;
        }

        #configuration {
            width: 320px;
            padding: 20px;
            background-color: #333;
            color: white;
            transition: 0.2s;
            box-shadow: -2px 0 5px rgba(0, 0, 0, 0.5);
            z-index: 3;
        }
        #configuration.collapsed {
            width: 0;
            padding: 20px 0;
            overflow: hidden;
        }

        /* Flag styles */
        .flag {
            position: fixed;
            top: 50%;
            width: 50px;
            height: 50px;
            background-color: rgb(165, 2, 2);  
            color: white;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            border-radius: 50%;
            transition: 0.2s;
            font-size: 28px;
            z-index: 5;
        }

        .right.flag{
            right: 345px;
        }

        .right.flag.collapsed {
            right: 0;
            border-radius: 5px 0 0 5px;
        }

    </style>
	
	<script>
	var options = {
        edges: {
          width: 5,
          font: {
            size: 12,
            color: "#C9C9C9",
          },
          arrows: {
            to: {
              enabled: false,
              scaleFactor: 1,
              type: 'arrow'
            },
            middle: {
              enabled: false,
              scaleFactor: 1,
              type: 'arrow'
            },
            from: {
              enabled: false,
              scaleFactor: 1,
              type: 'circle'
            }
          },
          scaling: {
            label: true,
          },
          dashes: false,
          shadow: false,
          smooth: false,
          color: {
            color: "#828282",
            highlight: "#D93E3E"
          },
          background: {
            enabled: false,
            color: "#00ff00",
          },
        },
        nodes: {
			shape: "box",
        },
        groups: {
          DOMAIN: {
            borderWidth: 2,
            shape: "box",
            size: 50,
            font: {
              size: 30,
              color: "#000000"
            }
          },
          PROJECT: {
            borderWidth: 2,
            shape: "box",
            size: 30,
            font: {
              size: 30,
              color: "#000000"
            }
          },
          ARCHETYPE: {
            borderWidth: 2,
            shape: "box",
            size: 30,
            font: {
              size: 30,
              color: "#000000"
            }
          },
          TEMPLATE: {
            borderWidth: 2,
            shape: "box",
            size: 30,
            font: {
              size: 30,
              color: "#000000"
            }
          }
        },
         physics: {
          forceAtlas2Based: {
            gravitationalConstant: -2500, // the amount of gravitation that draws nodes together (negative: they thry to escape from each other)
            centralGravity: 0.005, // gravity toward center
            springLength: 100,
            springConstant: 0.018,
          },
          maxVelocity: 146,
          solver: "forceAtlas2Based",
          timestep: 0.35,
          stabilization: {
            iterations: 15
          },
        },
      };
	</script>
	
</head>
<body>

    <div id="mainContent">
        
            <div id="headerOverlay">
                    <h1>{{CKMURL}}</h1>
					<p>{{PUBLICPRIVAT}}<br>
					{{STATE}}</p>
			</div>
			
			<div id="infoOverlay">
                <p>(c) 2024, CatSalut. Servei Català de la Salut 
				<br>
				License: <a href="https://www.apache.org/licenses/LICENSE-2.0">Apache 2.0</a>
				</p>
            </div>
			
		<div id="network"></div>
		
        <div id="configuration" class="collapsed">
            <h2>OPTIONS</h2>
			<hr>
			<h3>Configuration</h3>
			
			<input type="checkbox" id="smoothToggle"  onclick="toggleSmooth()"> Smooth edges<br><br>
			
            <input type="checkbox" id="physicsToggle" checked onclick="togglePhysics()"> Enable physics<br><br>

            <label for="repulsion">Gravitational constant:</label>
            <input type="range" id="repulsion" min="-10000" max="0" value="-2500" oninput="updatePhysics()">
			<span id="repulsionValue">-2500</span>
			<br><br>

            <label for="centralGravity">Central gravity:</label>
            <input type="range" id="centralGravity" min="0" max="0.1" step="0.0001" value="0.005" oninput="updatePhysics()">
			<span id="centralGravityValue">0.005</span>
			<br><br>
			
			<label for="springLength">Spring length:</label>
            <input type="range" id="springLength" min="1" max="500" step="1" value="100" oninput="updatePhysics()">
			<span id="springLengthValue">100</span>
			<br><br>
			
			<label for="springConstant">Spring constant:</label>
            <input type="range" id="springConstant" min="0.001" max="0.1" step="0.001" value="0.018" oninput="updatePhysics()">
			<span id="springConstantValue">0.018</span>
			<br><br>
			
			<hr>
			<h3>Shortcuts</h3>
			
			<p>Select a domain, project, template or archetype to jump to it.</p>
			
			<label for="domainSelect">Select a domain:</label>
            <select id="domainSelect">
                <option value="">-- Select a Domain --</option>
                <!-- Options will be populated dynamically -->
            </select>
            <br><br>
			
            <label for="projectSelect">Select a project:</label>
            <select id="projectSelect">
                <option value="">-- Select a Project --</option>
                <!-- Options will be populated dynamically -->
            </select>
            <br><br>
			
			<label for="templateSelect">Select a template:</label>
            <select id="templateSelect">
                <option value="">-- Select a Template --</option>
                <!-- Options will be populated dynamically -->
            </select>
            <br><br>
 
            <label for="archetypeSelect">Select an archetype:</label>
            <select id="archetypeSelect">
                <option value="">-- Select an Archetype --</option>
                <!-- Options will be populated dynamically -->
            </select>
            <br><br>
         </div>
    </div>

    <div class="flag right collapsed" id="flagRight"><i class='bx bx-cog' ></i></div>

    <script>
        // JavaScript for collapsing and expanding sidebar
        const sidebarRight = document.getElementById('configuration');
        const flagRight = document.getElementById('flagRight');

        flagRight.addEventListener('click', function() {
            // Toggle the collapsed class on both the sidebar and flag
            sidebarRight.classList.toggle('collapsed');
            flagRight.classList.toggle('collapsed');
        });
		"""

		content3 = """
		nodesOrigin.sort((a, b) => a.title.localeCompare(b.title));
		var container = document.getElementById('network');
		
		var nodes = new vis.DataSet(nodesOrigin); 
		var edges = new vis.DataSet(edgesOrigin);

        var data = {
            nodes: nodes,
            edges: edges
        };

        var network = new vis.Network(container, data, options);
		
		// Store the initial colors of the nodes
        var initialColors = {};
        nodes.forEach(node => {
            initialColors[node.id] = node.color;
        });
				
		var projectSelect = document.getElementById('projectSelect');
        nodesOrigin.forEach(function(node) {
            if (node.group === 'PROJECT') {
                var option = document.createElement('option');
                option.value = node.id;
				//option.text = node.label;
                option.text = node.label.replace('PROJECT:', '');
				option.text = option.text.replace('INCUBATOR:', '').substring(0, 40);
                projectSelect.add(option);
            }
        });
		
		// Add an event listener to the selection box
        projectSelect.addEventListener('change', function() {
            var selectedProjectId = this.value;
			resetOtherFields('projectSelect');
			resetNodeColors() ;
            // Highlight the selected project
            if (selectedProjectId) {
                var selectedNode = data.nodes.get(selectedProjectId);
                selectedNode.color = {background: '#FFFF00', border: '#FF0000'};
                data.nodes.update(selectedNode);
                network.focus(selectedProjectId, {
                    scale: 0.5,
                    animation: {
                        duration: 1000,
                        easingFunction: 'easeInOutQuad'
                    }
                });
            }
        });
		
	    var domainSelect = document.getElementById('domainSelect');
        nodesOrigin.forEach(function(node) {
            if (node.group === 'DOMAIN') {
                var option = document.createElement('option');
                option.value = node.id;
                option.text = node.label.replace('Subdomain:', '').substring(0, 40);
                domainSelect.add(option);
            }
        });
		
		// Add an event listener to the selection box
        domainSelect.addEventListener('change', function() {
            var selectedDomainId = this.value;
			resetOtherFields('domainSelect');
			resetNodeColors() ;
            // Highlight the selected project
            if (selectedDomainId) {
                var selectedNode = data.nodes.get(selectedDomainId);
                selectedNode.color = {background: '#FFFF00', border: '#FF0000'};
                data.nodes.update(selectedNode);
                network.focus(selectedDomainId, {
                    scale: 0.5,
                    animation: {
                        duration: 2000,
                        easingFunction: 'easeInOutQuad'
                    }
                });
            }
        });
		
		
		
		var templateSelect = document.getElementById('templateSelect');
        nodesOrigin.forEach(function(node) {
            if (node.group === 'TEMPLATE') {
                var option = document.createElement('option');
                option.value = node.id;
                option.text = node.label.replace('Template:', '').substring(0, 40);
                templateSelect.add(option);
            }
        });
		
		// Add an event listener to the selection box
        templateSelect.addEventListener('change', function() {
            var selectedTemplateId = this.value;
			resetOtherFields('templateSelect');
			resetNodeColors() ;
            // Highlight the selected project
            if (selectedTemplateId) {
                var selectedNode = data.nodes.get(selectedTemplateId);
                selectedNode.color = {background: '#FFFF00', border: '#FF0000'};
                data.nodes.update(selectedNode);
                network.focus(selectedTemplateId, {
                    scale: 0.5,
                    animation: {
                        duration: 2000,
                        easingFunction: 'easeInOutQuad'
                    }
                });
            }
        });
		
		
		var archetypeSelect = document.getElementById('archetypeSelect');
        nodesOrigin.forEach(function(node) {
            if (node.group === 'ARCHETYPE') {
                var option = document.createElement('option');
                option.value = node.id;
                option.text = node.label.replace('Archetype:', '').substring(0, 40);
                archetypeSelect.add(option);
            }
        });
		
		// Add an event listener to the selection box
        archetypeSelect.addEventListener('change', function() {
            var selectedArchetypeId = this.value;
			resetOtherFields('archetypeSelect');
			resetNodeColors() ;
            // Highlight the selected project
            if (selectedArchetypeId) {
                var selectedNode = data.nodes.get(selectedArchetypeId);
                selectedNode.color = {background: '#FFFF00', border: '#FF0000'};
                data.nodes.update(selectedNode);
                network.focus(selectedArchetypeId, {
                    scale: 0.5,
                    animation: {
                        duration: 2000,
                        easingFunction: 'easeInOutQuad'
                    }
                });
            }
        });
		


        // Function to update physics options
        function updatePhysics() {
            var repulsion = document.getElementById('repulsion').value;
            var centralGravity = document.getElementById('centralGravity').value;
			var springLength = document.getElementById('springLength').value;
			var springConstant = document.getElementById('springConstant').value;
		
			var isPhysicsEnabled = document.getElementById('physicsToggle').checked;
			

			const repulsionValue = document.getElementById('repulsionValue');
			const centralGravityValue = document.getElementById('centralGravityValue');
			const springLengthValue = document.getElementById('springLengthValue');
			const springConstantValue = document.getElementById('springConstantValue');
    
			// Update the displayed value
			repulsionValue.textContent = repulsion;
			centralGravityValue.textContent = centralGravity;
			springLengthValue.textContent = springLength;
			springConstantValue.textContent = springConstant;
				
            network.setOptions({
                physics: {
					enabled: isPhysicsEnabled,
                    forceAtlas2Based: {
						gravitationalConstant: repulsion,
                        centralGravity: centralGravity,
						springLength: springLength,
						springConstant: springConstant
                    },
					solver: 'forceAtlas2Based',
                }
            });
        }

        // Toggle the configuration panel visibility
        function toggleConfiguration() {
            var configPanel = document.getElementById('configuration');
            var networkDiv = document.getElementById('network');

            if (configPanel.style.display === "none") {
                configPanel.style.display = "block";
                networkDiv.style.width = "calc(100% - 300px)";
            } else {
                configPanel.style.display = "none";
                networkDiv.style.width = "100%";
            }

            network.redraw();
        }

        // Enable or disable physics based on checkbox state
        function togglePhysics() {
            var isPhysicsEnabled = document.getElementById('physicsToggle').checked;
			document.getElementById('repulsion').disabled = !isPhysicsEnabled;
			document.getElementById('centralGravity').disabled = !isPhysicsEnabled;
			document.getElementById('springLength').disabled = !isPhysicsEnabled;
			document.getElementById('springConstant').disabled = !isPhysicsEnabled;
            network.setOptions({
                physics: {
                    enabled: isPhysicsEnabled
                }
            });
        }
		
		// Enable or disable smooth edges
        function toggleSmooth() {
            var isSmoothEnabled = document.getElementById('smoothToggle').checked;
            network.setOptions({
                edges: {
                    smooth: isSmoothEnabled
                }
            });
        }

        // Highlight connected nodes and dim others
        network.on('click', function (params) {
        resetALLFields();
		if (params.nodes.length > 0) {
			var selectedNodeId = params.nodes[0];
			var connectedNodeIds = network.getConnectedNodes(selectedNodeId);

			const updatedNodes = nodes.map(node => {
				if (connectedNodeIds.includes(node.id) || node.id === selectedNodeId) {
					return {
						id: node.id,
						color: initialColors[node.id]
					};
				} else {
					return {
						id: node.id,
						color: {
							background: '#d3d3d3',
							border: "#d3d3d3",
							highlight: {
								background: "#d3d3d3",
								border: "#d3d3d3"
							}
						}
					};
				}
			});

			nodes.update(updatedNodes);
		} else{resetNodeColors();}
		});

		function resetNodeColors() {
			network.selectNodes([]);
			network.selectEdges([]);
			const updatedNodes = nodes.map(node => ({
				id: node.id,
				color: initialColors[node.id]
			}));
			nodes.update(updatedNodes);
		}

        function resetALLFields() {
            const dropdown1 = document.getElementById('domainSelect');
            const dropdown2 = document.getElementById('projectSelect');
			const dropdown3 = document.getElementById('templateSelect');
			const dropdown4 = document.getElementById('archetypeSelect');
            
            // Reset all fields except the one that was changed
			dropdown1.selectedIndex = 0;
			dropdown2.selectedIndex = 0;
			dropdown3.selectedIndex = 0;
			dropdown4.selectedIndex = 0;
        }

        function resetOtherFields(changedDropdownId) {
            const dropdown1 = document.getElementById('domainSelect');
            const dropdown2 = document.getElementById('projectSelect');
            const dropdown3 = document.getElementById('templateSelect');
			const dropdown4 = document.getElementById('archetypeSelect');
            
            // Reset all fields except the one that was changed
            if (changedDropdownId !== 'domainSelect') dropdown1.selectedIndex = 0;
            if (changedDropdownId !== 'projectSelect') dropdown2.selectedIndex = 0;
            if (changedDropdownId !== 'templateSelect') dropdown3.selectedIndex = 0;
			if (changedDropdownId !== 'archetypeSelect') dropdown4.selectedIndex = 0;
        }
    </script>
		
    
</body>
</html>
"""
		from base64 import b64encode

		def basic_auth(username, password):
			token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
			return f'Basic {token}'

		baseurl = entry_url.get()

		#correct the baseurl
		if baseurl[-1] != '/':
			baseurl+='/'
		if baseurl[-4:]=='ckm/':
			baseurl = baseurl[:-4]


		user = entry_user.get()
		pw = entry_password.get()


		header = { 'Authorization' : basic_auth(user, pw) }
		print(header)

		userisvalid = modules.test_user(baseurl, header)

		if not userisvalid:
			add_message('User authentication failed! Gathering only public data.')
			header = {}

		#****************************************      PART 1 - DOWNLOAD INFO FROM CKM  ***************************************

		add_message('Getting subdomains.\n')

		# create a dataframe with all subdomains
		XML = modules.get_XML_from_CKM(baseurl + '/ckm/rest/v1/subdomains',header)
		parameters = ['name', 'cid', 'description']
		df_subdomains = pd.DataFrame(columns=parameters)
		for i in range(len(XML)):
			value_list = []
			for p in parameters:
				value_list.append(XML[i].find(p).text)
			df_subdomains.loc[len(df_subdomains)] = value_list

		add_message('Getting projects.\n')
		# create a dataframe with all projects and subdomains
		XML = modules.get_XML_from_CKM(baseurl + '/ckm/rest/v1/projects',header)
		parameters = ['name', 'cid', 'subdomainName' ,'cidSubdomain','remoteSubdomain','description','projectType','public','forOrderTemplates']
		df_projects = pd.DataFrame(columns=parameters)
		for i in range(len(XML)):
			value_list = []
			for p in parameters:
				value_list.append(XML[i].find(p).text)
			df_projects.loc[len(df_projects)] = value_list

		add_message('Getting archetypes.\n')
		#create a dataframe with all archetypes
		XML = modules.get_XML_from_CKM_size(baseurl + '/ckm/rest/v1/archetypes',header,100)
		parameters = ['resourceMainId', 'resourceMainDisplayName', 'cid', 'projectName', 'cidProject','resourceType',
					  'status',
					  'creationTime',
					  'modificationTime',
					  'versionAsset',
					  'versionAssetLatest',
					  'uid',
					  'buildUid',
					  'revision',
					  'revisionLatest']
		df_archetypes = pd.DataFrame(columns=parameters)
		for i in range(len(XML)):
			value_list = []
			for p in parameters:
				if XML[i].find(p) is not None:
					value_list.append(XML[i].find(p).text)
				else:
					value_list.append('')
			df_archetypes.loc[len(df_archetypes)] = value_list

		add_message('Getting templates.\n')
		#create a dataframe with all templates
		XML = modules.get_XML_from_CKM_size(baseurl + '/ckm/rest/v1/templates',header,100)
		parameters = ['resourceMainDisplayName', 'cid', 'projectName', 'cidProject','resourceType',
					  'templateType',
					  'resourceMainId',
					  'status',
					  'creationTime',
					  'modificationTime',
					  'versionAsset',
					  'versionAssetLatest']
		df_templates = pd.DataFrame(columns=parameters)
		for i in range(len(XML)):
			value_list = []
			for p in parameters:
				value_list.append(XML[i].find(p).text)
			df_templates.loc[len(df_templates)] = value_list

		add_message('Getting required archetypes.\n')
		template_cid_list = list(df_templates['cid'])
		template_name_list = list(df_templates['resourceMainDisplayName'])

		parameters = ['resourceMainId', 'resourceMainDisplayName', 'cid','resourceType',
					  'status',
					  'creationTime',
					  'modificationTime',
					  'versionAsset',
					  'versionAssetLatest',
					  'revision',
					  'revisionLatest']
		df_required_archetypes = pd.DataFrame(columns=parameters+['template_DisplayName', 'template_cid'])

		for j in range(len(template_cid_list)):
			add_message(template_name_list[j]+'\n')
			#create a dataframe with all required archetypes for templates
			XML = modules.get_XML_from_CKM(baseurl + '/ckm/rest/v1/templates/'+ template_cid_list[j] + '/required-archetypes',header)
			for i in range(len(XML)):
				value_list = []
				for p in parameters:
					if XML[i].find(p) is not None:
						value_list.append(XML[i].find(p).text)
					else:
						value_list.append('')
				df_required_archetypes.loc[len(df_required_archetypes)] = value_list + [template_name_list[j], template_cid_list[j]]


		df_subdomains = df_subdomains.rename(columns={"name": "subdomain_name", "cid": "subdomain_cid"})
		df_projects = df_projects.rename(columns={'name': 'project_name', 'cid': 'project_cid', 'subdomainName': 'subdomain_name' ,'cidSubdomain': 'subdomain_cid'})
		df_archetypes = df_archetypes.rename(columns={'resourceMainId':'archetype_id', 'resourceMainDisplayName':'archetype_name', 'cid':'archetype_cid', 'projectName':'project_name', 'cidProject':'project_cid'})
		df_templates = df_templates.rename(columns={'resourceMainDisplayName': 'template_name', 'cid':'template_cid', 'projectName':'project_name', 'cidProject':'project_cid'})
		df_required_archetypes = df_required_archetypes.rename(columns={'resourceMainId':'archetype_id', 'resourceMainDisplayName':'archetype_name', 'cid': 'archetype_cid','template_DisplayName':'template_name', 'template_cid':'template_cid'})

		#*****************************         PART 2 - VIS.JS MODEL  ********************************************************

		resources = {}

		resources['subdomain'] = {}
		for i in df_subdomains.index:
			dict = {}
			dict['subdomain_name'] = df_subdomains.loc[i,'subdomain_name']
			dict['node_id'] = 'dom' + str(i)
			resources['subdomain'][df_subdomains.loc[i,'subdomain_cid']]=dict

		resources['project'] = {}
		for i in df_projects.index:
			dict = {}
			dict['project_name'] = df_projects.loc[i,'project_name']
			dict['subdomain_cid'] = df_projects.loc[i,'subdomain_cid']
			dict['subdomain_name'] = df_projects.loc[i,'subdomain_name']
			dict['node_id'] = 'proj' + str(i)
			dict['projectType'] = df_projects.loc[i,'projectType']
			dict['public'] = df_projects.loc[i,'public']
			resources['project'][df_projects.loc[i,'project_cid']]=dict

		resources['archetype'] = {}
		for i in df_archetypes.index:
			dict = {}
			dict['archetype_name'] = df_archetypes.loc[i,'archetype_name']
			dict['archetype_id'] = df_archetypes.loc[i,'archetype_id']
			dict['project_cid'] = df_archetypes.loc[i,'project_cid']
			dict['project_name'] = df_archetypes.loc[i,'project_name']
			dict['node_id'] = 'arch' + str(i)
			dict['status'] = df_archetypes.loc[i,'status']
			dict['revision'] = df_archetypes.loc[i,'revision']
			dict['revisionLatest'] = df_archetypes.loc[i,'revisionLatest']
			dict['creationTime'] = df_archetypes.loc[i,'creationTime']
			dict['modificationTime'] = df_archetypes.loc[i,'modificationTime']
			dict['uid'] = df_archetypes.loc[i,'uid']
			resources['archetype'][df_archetypes.loc[i,'archetype_cid']]=dict

		resources['template'] = {}
		for i in df_templates.index:
			dict = {}
			dict['template_name'] = df_templates.loc[i,'template_name']
			#dict['archetype_id'] = df_templates.loc[i,'archetype_id']
			df_search = df_required_archetypes[df_required_archetypes['template_cid']==df_templates.loc[i,'template_cid']]
			archetype_list = list(df_search['archetype_cid'])
			dict['project_cid'] = df_templates.loc[i,'project_cid']
			dict['project_name'] = df_templates.loc[i,'project_name']
			dict['node_id'] = 'temp' + str(i)
			dict['archetypes'] = archetype_list
			dict['templateType'] = df_templates.loc[i,'templateType']
			dict['status'] = df_templates.loc[i,'status']
			dict['creationTime'] = df_templates.loc[i,'creationTime']
			dict['modificationTime'] = df_templates.loc[i,'modificationTime']
			dict['resourceMainId'] = df_templates.loc[i,'resourceMainId']
			resources['template'][df_templates.loc[i,'template_cid']]=dict

		node_list=[]
		#FORMAT {'id': 'org0', 'label': 'Agencia Estatal Consejo\nSuperior De Investigaciones\nCientificas (CSIC)', 'title': 'Countr...'},
		import math
		key_list = list(resources['subdomain'].keys())
		for k in range(len(key_list)):
			key = key_list[k]
			node = {}
			node['id'] = resources['subdomain'][key]['node_id']
			node['label'] = 'Subdomain:\n' + resources['subdomain'][key]['subdomain_name']
			node['title'] = resources['subdomain'][key]['subdomain_name'] + '\n' + 'cid: ' + str(key)
			node['group'] = 'DOMAIN'
			node_list.append(node)

		key_list = list(resources['project'].keys())
		for k in range(len(key_list)):
		#for key in resources['project']:
			key = key_list[k]
			node = {}
			node['id'] = resources['project'][key]['node_id']
			node['label'] = resources['project'][key]['projectType']+ ':\n' + resources['project'][key]['project_name']
			node['title'] = resources['project'][key]['project_name']  + '\n' + 'cid: ' + str(key) + '\n' + 'subdomain: ' + resources['project'][key]['subdomain_name'] + '\n' + 'projectType: ' + resources['project'][key]['projectType'] + '\n' + 'public: ' + resources['project'][key]['public']
			node['group'] = 'PROJECT'
			node_list.append(node)

		key_list = list(resources['archetype'].keys())
		for k in range(len(key_list)):
		#for key in resources['archetype']:
			key = key_list[k]
			node = {}
			node['id'] = resources['archetype'][key]['node_id']
			shortened_id = resources['archetype'][key]['archetype_id'].replace('openEHR-EHR-','...\n')
			node['label'] = 'Archetype:\n' + resources['archetype'][key]['archetype_name'] + '\n' + shortened_id
			node['title'] = resources['archetype'][key]['archetype_name'] + '\n' + resources['archetype'][key]['archetype_id'] + '\n' + 'cid: ' + str(key) + '\n' + 'project: ' + resources['archetype'][key]['project_name'] + '\n' + 'status: ' + resources['archetype'][key]['status'] + '\n' + 'revision: ' + resources['archetype'][key]['revision'] + '\n' + 'revisionLatest: ' + resources['archetype'][key]['revisionLatest'] + '\n' + 'creationTime: ' + resources['archetype'][key]['creationTime'] + '\n' + 'modificationTime: ' + resources['archetype'][key]['modificationTime']+ '\n' + 'uid: ' + resources['archetype'][key]['uid']
			node['group'] = 'ARCHETYPE'
			node_list.append(node)

		key_list = list(resources['template'].keys())
		for k in range(len(key_list)):
		#for key in resources['template']:
			key = key_list[k]
			node = {}
			node['id'] = resources['template'][key]['node_id']
			node['label'] = 'Template:\n' + resources['template'][key]['template_name']
			node['label'] = node['label'].replace('[','')
			node['label'] = node['label'].replace(']','')

			node['title'] = resources['template'][key]['template_name']+ '\n' +'cid: ' + str(key) + '\n' + 'project: ' + resources['template'][key]['project_name'] + '\n' + 'templateType: ' + resources['template'][key]['templateType'] + '\n' + 'status: ' + resources['template'][key]['status'] + '\n' + 'creationTime: ' + resources['template'][key]['creationTime'] + '\n' + 'modificationTime: ' + resources['template'][key]['modificationTime']+ '\n' + 'resourceMainId: ' + resources['template'][key]['resourceMainId']
			node['title'] = node['title'].replace('[','')
			node['title'] = node['title'].replace(']','')

			node['group'] = 'TEMPLATE'
			node_list.append(node)

		#make edges
		#  FORMAT: {'from': 'org122', 'to': 'proj0', 'label': 'EU-funded consortium', 'title': 'EU-funded consortium'},
		edge_list = []
		for key in resources['project']:
			node = {}
			fro = resources['project'][key]['node_id']
			to = resources['subdomain'][resources['project'][key]['subdomain_cid']]['node_id']
			node['from'] = fro
			node['to'] = to
			node['label'] = ''
			node['title'] = ''
			edge_list.append(node)

		for key in resources['archetype']:
			node = {}
			fro = resources['archetype'][key]['node_id']
			to = resources['project'][resources['archetype'][key]['project_cid']]['node_id']
			node['from'] = fro
			node['to'] = to
			node['label'] = ''
			node['title'] = ''
			edge_list.append(node)

		for key in resources['template']:
			node = {}
			fro = resources['template'][key]['node_id']
			to = resources['project'][resources['template'][key]['project_cid']]['node_id']
			node['from'] = fro
			node['to'] = to
			node['label'] = ''
			node['title'] = ''
			edge_list.append(node)

		for key in resources['template']:
			fro = resources['template'][key]['node_id']
			for i in range(len(resources['template'][key]['archetypes'])):
				if resources['template'][key]['archetypes'][i] in resources['archetype'].keys():
					node = {}
					to = resources['archetype'][resources['template'][key]['archetypes'][i]]['node_id']
					node['from'] = fro
					node['to'] = to
					node['label'] = ''
					node['title'] = ''
					edge_list.append(node)
				pass

		result_string = 'var nodesOrigin =' +str(node_list) + '\nvar edgesOrigin =' + str(edge_list)
		result_string = result_string.replace('[','\n[')
		result_string = result_string.replace('},','},\n')

		from datetime import date

		today = date.today()
		date_today = today.strftime("%d/%m/%Y")
		date_file = today.strftime("%y%m%d")

		n_domains = len(resources['subdomain'].keys())
		n_projects = len(resources['project'].keys())
		n_archetypes = len(resources['archetype'].keys())
		n_templates = len(resources['template'].keys())

		content1 = content1.replace('{{STATE}}','State: '+date_today+'. Domains: '+str(n_domains) +', Projects: '+str(n_projects) + ', Archetypes: '+str(n_archetypes) + ', Templates: '+str(n_templates)+'. ')
		content1 = content1.replace('{{CKMURL}}', entry_url.get())

		#create text for PUBLIC or accessed with user
		if not userisvalid:
			pub_priv = 'Public repository only!'
		else:
			pub_priv = 'Repository accessed by user: ' + entry_user.get()

		content1 = content1.replace('{{PUBLICPRIVAT}}', pub_priv)


		#ADD COLOR TO EVERY NODE
		result_string = result_string.replace("'group': 'DOMAIN'", "'group': 'DOMAIN', color: {background: '#9F9F9F', border: '#414141', highlight: {background: '#D8D8D8', border: '#D93E3E'}}")
		result_string = result_string.replace("'group': 'PROJECT'","'group':'PROJECT', color: {background: '#FF4949', border: '#651D1D', highlight: {background: '#FFB1B1', border: '#D93E3E'}}")
		result_string = result_string.replace("'group': 'TEMPLATE'","'group':'TEMPLATE', color: {background: '#FDB322', border: '#391B00', highlight: {background: '#FECA64', border: '#D93E3E'}}")
		result_string = result_string.replace("'group': 'ARCHETYPE'","'group':'ARCHETYPE', color: {background: '#5EB6E5', border: '#00375F', highlight: {background: '#BDE3F6', border: '#D93E3E'}}")

		add_message('Writing to HTML file...'+'\n')
		# Open the destination file
		destination_dir = output_folder  + date_file+'_CKM-resource-vis_embedded.html'
		destination_file = open(destination_dir, 'w', encoding='utf-8')
		# Write the concatenated content to the destination file
		destination_file.write('\ufeff'+content1 + result_string + content3)
		# Close the destination file
		add_message('Done!'+'\n')
		destination_file.close()
		webbrowser.open(destination_dir)
		return destination_dir

	def add_message(phrase):
		message_box.insert('end',phrase)
		message_box.see("end")
		root.update()

	def select_folder():
		input_folder_path = filedialog.askdirectory()
		if input_folder_path:
			entry_box.delete("0.0", "end")
			entry_box.insert("0.0",input_folder_path)
			generate_btn.configure(state="normal")

	customtkinter.set_appearance_mode("dark")   #dark, system or light
	customtkinter.set_default_color_theme("green") #blue, green or dark-blue

	root = customtkinter.CTk()
	root.geometry("420x690")
	root.title('CKM content visualization')
	root.minsize(420,690)
	root.maxsize(420,690)

	frame = customtkinter.CTkFrame(root)
	frame.pack(pady=10, padx=10, fill = "both", expand = True)

	label = customtkinter.CTkLabel(frame, text = "CKM content visualization", font = ("Roboto", 24))
	label.pack(pady = 10)

	customtkinter.CTkLabel(frame, text = "Destination folder", font = ("Roboto", 12)).pack()
	entry_box = customtkinter.CTkTextbox(frame, width=400, height=80)
	entry_box.pack(pady = (0,10))

	folder_btn = customtkinter.CTkButton(frame, text="Select folder for the HTML file...", command= select_folder)
	folder_btn.pack(pady = 10)

	customtkinter.CTkLabel(frame, text = "CKM URL (example: https://ckm.salut.gencat.cat/)", font = ("Roboto", 12)).pack()
	entry_url = customtkinter.CTkEntry(
                frame,
                width=350,
                height=30,
                border_width=1,
                fg_color="white",
                placeholder_text="CKM URL",
                text_color="black",
                font=('Arial Rounded MT Bold', 12))
	entry_url.pack(pady = (0,10))

	customtkinter.CTkLabel(frame, text = "Username (optional)", font = ("Roboto", 12)).pack()
	entry_user = customtkinter.CTkEntry(
                frame,
                width=200,
                height=30,
                border_width=1,
                fg_color="white",
                placeholder_text="OPTIONAL: Username",
                text_color="black",
                font=('Arial Rounded MT Bold', 12))
	entry_user.pack(pady = (0,10))

	customtkinter.CTkLabel(frame, text = "Password (optional)", font = ("Roboto", 12)).pack()
	entry_password = customtkinter.CTkEntry(
                frame,
                width=200,
                height=30,
                border_width=1,
                fg_color="white",
                placeholder_text="OPTIONAL: Enter password...",
                show="*",
                text_color="black",
                font=('Arial Rounded MT Bold', 12))
	entry_password.pack(pady = (0,10))

	entry_url.insert(0, "https://ckm.salut.gencat.cat/")

	generate_btn = customtkinter.CTkButton(frame, text="Generate HTML...", command=lambda: make_visualization(entry_box.get("0.0", "end").strip()+"/"))
	generate_btn.configure(state="disabled")
	generate_btn.pack(pady = 10)

	message_box = customtkinter.CTkTextbox(frame, width=380, height=180)
	message_box.pack(pady = 10)
	about = "(c) 2024, CatSalut. Servei Català de la Salut\nLicense: Apache 2.0\n"
	message_box.insert('end',about)

	root.mainloop()

def main():

	my_gui()

if __name__ == "__main__":
	import modules
	main()
else:
	import Projects.CKM_List_all_resources_universal_v0_1.modules as modules
