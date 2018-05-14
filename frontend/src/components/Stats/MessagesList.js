import React, { Component } from 'react'
import Modal from 'react-modal'

import './MessagesList.css'

class MessagesList extends Component {
	render() {
		if (this.props.isDataLoading) {
			return (
				<div className="container">
					<div className="card">
						<div className="card-body">
							<div className="card-text text-center">Loading...</div>
						</div>
					</div>
				</div>
			);
		}

		if (this.props.messages.length === 0) {
			return (
				<div className="container">
					<div className="card">
						<div className="card-body">
							<div className="card-text text-center">Nothing has been found...</div>
						</div>
					</div>
				</div>
			);
		}

		return (
			<div className="container">
				<div id="scrolling">
					{this.props.messages.map((message, index) => (
						<MessageItem key={index} value={message}/>
					))}
				</div>
			</div>
		);
	}
}

export default MessagesList;

Modal.setAppElement('body');

class MessageItem extends Component {
	constructor (props) {
		super(props);
		this.state = {
			showModal: false,
			isDataLoaded: false,
			data: { "text" : this.props.value["summary"]}
		};
	
		this.handleOpenModal = this.handleOpenModal.bind(this);
		this.handleCloseModal = this.handleCloseModal.bind(this);
	}

	loadData() {
		// this.setState( {data : {"text" : "LLVM can provide the middle layers of a complete compiler system, taking intermediate representation (IR) code from a compiler and emitting an optimized IR. This new IR can then be converted and linked into machine-dependent assembly language code for a target platform. LLVM can accept the IR from the GNU Compiler Collection (GCC) toolchain, allowing it to be used with a wide array of extant compilers written for that project. LLVM can also generate relocatable machine code at compile-time or link-time or even binary machine code at run-time. LLVM supports a language-independent instruction set and type system.[17] Each instruction is in static single assignment form (SSA), meaning that each variable (called a typed register) is assigned once and then frozen. This helps simplify the analysis of dependencies among variables. LLVM allows code to be compiled statically, as it is under the traditional GCC system, or left for late-compiling from the IR to machine code via just-in-time compilation (JIT), similar to Java. The type system consists of basic types such as integer or floating point numbers and five derived types: pointers, arrays, vectors, structures, and functions. A type construct in a concrete language can be represented by combining these basic types in LLVM. For example, a class in C++ can be represented by a mix of structures, functions and arrays of function pointers. The LLVM JIT compiler can optimize unneeded static branches out of a program at runtime, and thus is useful for partial evaluation in cases where a program has many options, most of which can easily be determined unneeded in a specific environment. This feature is used in the OpenGL pipeline of Mac OS X Leopard (v10.5) to provide support for missing hardware features.[18] Graphics code within the OpenGL stack can be left in intermediate representation, and then compiled when run on the target machine. On systems with high-end graphics processing units (GPUs), the resulting code remains quite thin, passing the instructions on to the GPU with minimal changes. On systems with low-end GPUs, LLVM will compile optional procedures that run on the local central processing unit (CPU) that emulate instructions that the GPU cannot run internally. LLVM improved performance on low-end machines using Intel GMA chipsets. A similar system was developed under the Gallium3D LLVMpipe, and incorporated into the GNOME shell to allow it to run without a proper 3D hardware driver loaded."} })	
		var query = this.props.value

		fetch('http://localhost:8000/letters/?get_text=1&source=' 
				+ query["source"] + '&target=' + query["target"] 
				+ '&date=' + query["date"] + '&topic=' + query["topic"])
			.then(response => response.json())
			.then(data => this.setState({ data: data["0"]}));
	}

	handleOpenModal () {
		if (!this.state.isDataLoaded) {
			this.loadData();
			this.setState( {isDataLoaded : true} );
		}

		this.setState({ showModal: true });
	}

	handleCloseModal () {
		this.setState({ showModal: false });
	}

	render() {
		var dateFormat = require('dateformat');
		var date = this.props.value["date"]

		return (
		<div>
		
		<div className="card" onClick={this.handleOpenModal}>
			<div className="card-body">
				<div className="pull-left">
					<h6>{ this.props.value["source"].slice(0, 10) }</h6>
				</div>
				
				<div className="pull-right">
					<h6 className="text-right">{ dateFormat(date, "shortDate") }</h6>
				</div>
				
				<div className="clearfix"></div>

				<p className="card-text"  fontSize="5">
					{this.props.value["summary"].slice(0, 100) }
				</p>
			</div>
		</div>

		<Modal isOpen={this.state.showModal} onRequestClose={this.handleCloseModal} style={customStyles}>
			
			<button onClick={this.handleCloseModal} type="button" class="close" aria-label="Close">
				<span aria-hidden="true">&times;</span>
			</button>
					
			<dl className="row">
				<dt className="col-sm-2">
					<p className="font-italic"> From </p>
				</dt>

				<dd className="col-sm-10">
					{this.props.value["source"]}
				</dd>
				
				<dt className="col-sm-2">
					<p className="font-italic">To</p>
				</dt>
				<dd className="col-sm-10">{this.props.value["target"]}</dd>

				<dd className="col-sm-10"> 
					<p className="font-weight-bold">
						{dateFormat(date, "default")}
					</p> 
				</dd>
			</dl>

			<p className="font-weight-light">
				{this.state.data["text"]}
			</p>
		</Modal>
		</div>
		);
	}
}

const customStyles = {
	content : {
		top : '10%',
		left : '20%',
		right : '20%',
		bottom : '10%'
	}
};