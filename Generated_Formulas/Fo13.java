/**
 * Copyright (C) 2020 GZoltar contributors.
 * 
 * This file is part of GZoltar.
 * 
 * GZoltar is free software: you can redistribute it and/or modify it under the terms of the GNU
 * Lesser General Public License as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 * 
 * GZoltar is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
 * the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
 * General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License along with GZoltar. If
 * not, see <https://www.gnu.org/licenses/>.
 */
package com.gzoltar.sfl.formulas;

/**
 * Implementation of Ochiai coefficient from <i>Zoogeographic studies on the soleoid fishes found in
 * Japan and its neighbouring regions<i>.
 * 
 * @author José Campos
 */ 

public final class Fo13 extends AbstractSFLFormula{
	 @Override
 	 public String getName() {
 	 return "Fo13";
 	}
 	 @Override
 	 public double compute(final double n00, final double n01, final double n10, final double n11) {
 	 	 try { 
 	 	 return n10*(n00 + n11)/(n00 + n01 + n10 + n11); 
 	 	 }
 	 	 catch(ArithmeticException e){
 	 	 	 return 0.0; 
 	 	 }
 	 	 
 	 }
}
