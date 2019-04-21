package com.interview.prep;

public class BinaryTreeHeight {

	static class Node {
		int data;
		Node right, left;

		Node(int data) {
			this.data = data;
			left = right = null;
		}

	}

	Node root;

	public int maxHeight(Node node) {

		if (node == null) {
			return 0;
		} else {
			int lheight = maxHeight(node.left);
			int rheight = maxHeight(node.right);
			return 1 + Math.max(lheight, rheight);
		}

	}
	
	public void printBinaryTree(Node root){
		if(root==null)
			return;
			
			
			printBinaryTree(root.left);
			System.out.println(root.data);
			printBinaryTree(root.right);
		
	}

	public static void main(String[] args) {
		BinaryTreeHeight bth = new BinaryTreeHeight();
		bth.root = new Node(20);
		bth.root.left = new Node(40);
		System.out.println(bth.maxHeight(bth.root));
		bth.printBinaryTree(bth.root);
	}
}
