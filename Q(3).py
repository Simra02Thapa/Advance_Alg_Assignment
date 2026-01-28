class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class ServiceCenterTree:
    def __init__(self):
        self.service_centers = 0

    def minServiceCenters(self, root):
    # Returns the minimum number of service centers required
        root_state = self.dfs(root)

    # If root still needs service, place one more center
        if root_state == 0:
            self.service_centers += 1
            print("Service center placed at root")

        return self.service_centers

    def dfs(self, node):
        """
        DFS traversal
        State meanings:
        0 -> Node needs service
        1 -> Node has a service center
        2 -> Node is already covered
        """

        if node is None:
            return 2   # Null nodes are considered covered

        left_state = self.dfs(node.left)
        right_state = self.dfs(node.right)

        # If any child needs service, place service center here
        if left_state == 0 or right_state == 0:
            self.service_centers += 1
            print(f"Service center placed at node {node.value}")
            return 1

        # If any child has a service center, this node is covered
        if left_state == 1 or right_state == 1:
            return 2

        # Otherwise, this node needs service
        return 0


# Example Tree (as asked in the Question)

# Tree representation similar to:
# {0, 0, null, 0, null, 0, null, null, 0}

root = TreeNode(0)
root.left = TreeNode(0)
root.left.left = TreeNode(0)
root.left.left.left = TreeNode(0)
root.left.left.left.right = TreeNode(0)

#Run the Algorithm

tree = ServiceCenterTree()
result = tree.minServiceCenters(root)

print("Minimum service centers required by the Corporation:", result)
