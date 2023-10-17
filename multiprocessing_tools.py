def input_split(vals, cores):
	import numpy as np
	if len(vals.shape)>1:
		splits= np.split(vals[:len(vals)-len(vals)%cores], cores)
		if len(vals)%cores !=0:
			shape= (1, splits[0].shape[-1])
			for i, rem in enumerate(vals[len(vals)-(len(vals)%cores):]):
				splits[i]= np.append(splits[i], rem.reshape(shape), axis=0)
		return splits
	else:
		splits= np.split(vals[:len(vals)-len(vals)%cores], cores)
		if len(vals)%cores !=0:
			for i, rem in enumerate(vals[len(vals)-(len(vals)%cores):]):
				splits[i]=np.array([*splits[i], rem])
		return splits
