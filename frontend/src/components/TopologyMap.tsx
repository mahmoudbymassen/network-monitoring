import React, { useEffect, useState, useCallback } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  MiniMap, 
  Node, 
  Edge 
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Typography, Button, Box } from '@mui/material';
import { networkApi, TopologyNode, TopologyEdge, TopologyResponse } from '../services/api';

const TopologyMap = () => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [loading, setLoading] = useState(true);

  // Grid-based layout algorithm to prevent overlapping
  const calculateNodePositions = (nodeList: TopologyNode[], edgeList: TopologyEdge[]) => {
    const GRID_SIZE = 250; // Distance between nodes in the grid
    const NODES_PER_ROW = 4; // Number of nodes per row
    
    // Group nodes by floor for better organization
    const nodesByFloor: Map<number, TopologyNode[]> = new Map();
    
    nodeList.forEach((node) => {
      const floor = node.floor || 0;
      if (!nodesByFloor.has(floor)) {
        nodesByFloor.set(floor, []);
      }
      nodesByFloor.get(floor)!.push(node);
    });

    // Calculate positions based on floor groups
    const positions: Map<string | number, { x: number; y: number }> = new Map();
    let currentY = 100;

    Array.from(nodesByFloor.entries())
      .sort(([floorA], [floorB]) => floorA - floorB)
      .forEach(([floor, floorNodes]) => {
        let currentX = 100;
        let maxHeight = 0;

        floorNodes.forEach((node, index) => {
          positions.set(node.id.toString(), {
            x: currentX,
            y: currentY
          });

          currentX += GRID_SIZE;
          maxHeight = Math.max(maxHeight, 120);

          // Move to next row
          if ((index + 1) % NODES_PER_ROW === 0) {
            currentX = 100;
            currentY += maxHeight + 50;
            maxHeight = 0;
          }
        });

        // Space between floors
        currentY += maxHeight + 100;
      });

    return positions;
  };

  const fetchTopology = useCallback(async () => {
  try {
    setLoading(true);

    const topologyData: TopologyResponse = await networkApi.getTopology();

    // Support both possible response shapes: { nodes, edges } or { topology: { nodes, edges } }
    const nodesSource: TopologyNode[] = topologyData?.nodes ?? topologyData?.topology?.nodes ?? [];
    const edgesSource: TopologyEdge[] = topologyData?.edges ?? topologyData?.topology?.edges ?? [];

    // Calculate positions using grid-based layout
    const positionMap = calculateNodePositions(nodesSource, edgesSource);

    // Create Nodes
    const flowNodes: Node[] = nodesSource.map((node: TopologyNode) => {
      const position = positionMap.get(node.id.toString()) || { x: 100, y: 100 };
      
      return {
        id: node.id.toString(),
        position,
        data: {
          label: node.ip || node.adresse_ip || `Node ${node.id}`
        },
        style: {
          background: node.status === 'en_ligne' ? '#4caf50' : '#f44336',
          color: '#fff',
          borderRadius: '12px',
          padding: '12px 16px',
          border: '2px solid #333',
          fontSize: '12px',
          fontWeight: 500,
          minWidth: '120px',
          textAlign: 'center'
        }
      };
    });

    // Create Edges
    const flowEdges: Edge[] = edgesSource.map((edge: TopologyEdge, index: number) => ({
      id: `e${index}`,
      source: edge.from.toString(),
      target: edge.to.toString(),
      type: 'smoothstep',
      animated: true,
    }));

    setNodes(flowNodes);
    setEdges(flowEdges);

  } catch (error) {
    console.error("Error fetching topology:", error);
  } finally {
    setLoading(false);
  }
}, []);
  useEffect(() => {
    fetchTopology();
  }, [fetchTopology]);

  return (
    <Box sx={{ height: '85vh', width: '100%' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2, alignItems: 'center' }}>
        <Typography variant="h5">Network Topology Map</Typography>
        <Button variant="contained" onClick={fetchTopology}>
          Refresh Topology
        </Button>
      </Box>

      <ReactFlow 
        nodes={nodes} 
        edges={edges} 
        fitView
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </Box>
  );
};

export default TopologyMap;