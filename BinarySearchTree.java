package com.interview.prep;

public class BinarySearchTree {

	static class Node {
		int num;
		Node right, left;

		Node(int a) {
			this.num = a;
			this.right = this.left = null;
		}
	}

	Node root = null;

	public void insertBST(int data) {

		root = insert(root, data);

	}

	public Node insert(Node root, int data) {
		if (root == null) {
			root = new Node(data);
			return root;
		}

		if (root.num > data) {
			root.left = insert(root.left, data);
			System.out.println("Insert Left");
		} else if(root.num < data) {
			root.right = insert(root.right, data);
			System.out.println("Insert Right");
		}
		return root;
	}

	public void DisplayTree(Node root) {
		if (root == null)
			return;
		else {
			DisplayTree(root.left);
			System.out.println(root.num);
			DisplayTree(root.right);
		}
	}

	public static void main(String[] args) {
		BinarySearchTree bst = new BinarySearchTree();
		bst.insertBST(10);
		bst.insertBST(20);
		bst.insertBST(5);
		bst.insertBST(40);
		bst.insertBST(30);
		bst.insertBST(80);
		bst.insertBST(3);
		bst.DisplayTree(bst.root);
	}
}
